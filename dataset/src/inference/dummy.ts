import { wordToAlphabetPronunciation } from "../utils.ts";
import { InferenceProvider } from "./index.ts";

export class DummyInferenceProvider extends InferenceProvider {
  async infer(words: string[]) {
    const results = Object.fromEntries(
      words.map((word) => [word, wordToAlphabetPronunciation(word)]),
    );
    for (const word in results) {
      // たまに変な読み方の結果を混ぜる
      if (Math.random() < 0.001) {
        results[word] = word;
      }
      // たまにスキップする
      if (Math.random() < 0.001) {
        delete results[word];
      }
    }

    return results;
  }
}
