import { alphabetMap } from "../utils.ts";
import { InferenceProvider } from "./index.ts";

export class DummyInferenceProvider extends InferenceProvider {
  async infer(words: string[]) {
    const results = Object.fromEntries(
      words.map((word) => [word, this.convertToKatakana(word)]),
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

  private convertToKatakana(word: string) {
    return word
      .split("")
      .map(
        (char) =>
          alphabetMap[char.toLowerCase() as keyof typeof alphabetMap] ?? char,
      )
      .join("");
  }
}
