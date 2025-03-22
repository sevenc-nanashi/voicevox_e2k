import { InferenceProvider } from "./index.ts";

export class DummyInferenceProvider extends InferenceProvider {
  async infer(words: string[]) {
    return Object.fromEntries(
      words.map((word) => [word, this.convertToKatakana(word)]),
    );
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

const alphabetMap = {
  a: "エー",
  b: "ビー",
  c: "シー",
  d: "ディー",
  e: "イー",
  f: "エフ",
  g: "ジー",
  h: "エイチ",
  i: "アイ",
  j: "ジェー",
  k: "ケー",
  l: "エル",
  m: "エム",
  n: "エヌ",
  o: "オー",
  p: "ピー",
  q: "キュー",
  r: "アール",
  s: "エス",
  t: "ティー",
  u: "ユー",
  v: "ブイ",
  w: "ダブリュー",
  x: "エックス",
  y: "ワイ",
  z: "ゼット",
};
