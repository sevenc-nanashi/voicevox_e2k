import * as fs from "node:fs/promises";
import { Semaphore } from "@core/asyncutil/semaphore";
import * as inference from "./inference/index.ts";
import * as source from "./source/index.ts";
import { ExhaustiveError, bisectMax, normalizeKana, shuffle } from "./utils.ts";
import { load as loadYaml } from "js-yaml";
import { configSchema } from "./config.ts";

async function main() {
  const config = await loadConfig();

  let sourceProvider: source.SourceProvider;
  switch (config.source.provider) {
    case "cmudict":
      sourceProvider = new source.CmuDict();
      break;
    default:
      throw new ExhaustiveError(config.source.provider);
  }
  let inferenceProvider: inference.InferenceProvider;
  switch (config.inference.provider) {
    case "gemini":
      inferenceProvider = new inference.Gemini();
      break;
    default:
      throw new ExhaustiveError(config.inference.provider);
  }

  setSeed(config.randomSeed);

  console.log("1: Loading words...");
  const words = await loadWords(sourceProvider, config.source.maxNumWords);

  console.log("2: Finding maximum batch size...");
  const maxBatchSize = await findMaxBatchSize(inferenceProvider, words);
  const batchSize = maxBatchSize * 0.9;

  console.log("3: Inferring pronunciations...");
  const allResults = await inferPronunciations(
    inferenceProvider,
    config.inference.concurrency,
    words,
    batchSize,
  );

  console.log("4: Cleaning up results...");
  const cleanedResults = cleanUpResults(allResults);

  console.log("5: Writing results...");
  const path = `${import.meta.dirname}/../../train/vendor/data.jsonl`;
  await writeResults(path, cleanedResults);

  console.log(
    `${Object.keys(cleanedResults).length} pronunciations written to ${path}`,
  );
}

main().catch((err) => {
  console.error(String(err));
  process.exit(1);
});

async function loadConfig() {
  return configSchema.parse(
    loadYaml(
      await fs.readFile(`${import.meta.dirname}/../config.yml`, "utf-8"),
    ),
  );
}

async function loadWords(
  sourceProvider: source.SourceProvider,
  maxNumWords: number | "all",
) {
  let words = await sourceProvider.getWords();
  console.log(`Loaded ${words.length} words`);
  if (maxNumWords !== "all") {
    console.log(`Shuffling and limiting to ${maxNumWords} words...`);
    words = shuffle(words).slice(0, maxNumWords);
  }

  return words;
}

async function findMaxBatchSize(
  inferenceProvider: inference.InferenceProvider,
  words: string[],
) {
  const maxBatchSize = await bisectMax(1, 1000, async (batchSize) => {
    console.log(`Trying batch size ${batchSize}...`);
    const currentWords = shuffle(words).slice(0, batchSize);
    const results = await inferenceProvider.infer(currentWords).catch((err) => {
      console.error(String(err));
      return {};
    });
    return Object.keys(results).length === batchSize;
  });
  console.log(`Found maximum batch size: ${maxBatchSize}`);

  if (maxBatchSize < 10) {
    throw new Error(`Batch size too small: ${maxBatchSize}`);
  }
  return maxBatchSize;
}

async function inferPronunciations(
  inferenceProvider: inference.InferenceProvider,
  concurrency: number,
  words: string[],
  batchSize: number,
) {
  const semaphore = new Semaphore(concurrency);
  console.log(`Using ${concurrency} concurrency`);

  const promises: Promise<unknown>[] = [];
  const allResults: Record<string, string> = {};

  const shuffledWords = shuffle(words);

  const inferBatch = (words: string[]) =>
    semaphore.lock(async () => {
      try {
        const results = await inferenceProvider.infer(words);

        console.log(
          `Inferred ${Object.keys(results).length} pronunciations, ${shuffledWords.length - Object.keys(allResults).length} remaining`,
        );
        Object.assign(allResults, results);

        const remainingWords = words.filter((word) => !(word in results));
        if (remainingWords.length === 0) {
          return;
        }
        console.log(`Re-inferring ${remainingWords.length} words...`);
        promises.push(inferBatch(remainingWords));
      } catch (err) {
        if (String(err).includes("429")) {
          console.error("Rate limited, waiting 1 minute...");
          await new Promise((resolve) => setTimeout(resolve, 60000));

          console.error("Retrying inference...");
          promises.push(inferBatch(words));
          return;
        }
        const halfWords = words.slice(0, words.length / 2);
        const halfWords2 = words.slice(words.length / 2);
        console.error(String(err));
        promises.push(inferBatch(halfWords));
        promises.push(inferBatch(halfWords2));
        console.log(
          `Splitting batch of ${words.length} into two batches of ${halfWords.length} and ${halfWords2.length}`,
        );
      }
    });

  for (let i = 0; i < shuffledWords.length; i += batchSize) {
    const currentWords = shuffledWords.slice(i, i + batchSize);

    promises.push(inferBatch(currentWords));
  }

  let numRetries = 0;
  while (Object.keys(allResults).length < words.length) {
    await Promise.all(promises);
    numRetries++;
    if (numRetries > 10) {
      throw new Error("Too many retries");
    }
  }

  return allResults;
}

function cleanUpResults(results: Record<string, string>) {
  const cleanedResults: Record<string, string> = {};
  for (const [word, pronunciation] of Object.entries(results)) {
    const normalized = normalizeKana(pronunciation);
    if (!normalized.match(/^[\p{Script=Katakana}ー]+$/u)) {
      console.error(`Invalid pronunciation for ${word}: ${pronunciation}`);
    } else {
      cleanedResults[word] = normalized;
    }
  }

  return cleanedResults;
}

async function writeResults(path: string, results: Record<string, string>) {
  await fs.writeFile(
    path,
    Object.entries(results)
      .map(([word, pronunciation]) =>
        JSON.stringify({
          word,
          kata: [pronunciation],
        }),
      )
      .join("\n"),
  );
}
