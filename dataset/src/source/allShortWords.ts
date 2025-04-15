import { SourceProvider } from "./index.ts";

// すべてのアルファベットと、それを2つ組み合わせたものを生成する
export class AllShortWordsSourceProvider extends SourceProvider {
  async getWords() {
    const words = [];
    for (let i = -1; i < 26; i++) {
      for (let j = 0; j < 26; j++) {
        if (i === -1) {
          words.push(String.fromCharCode(97 + j));
        } else {
          words.push(String.fromCharCode(97 + i) + String.fromCharCode(97 + j));
        }
      }
    }

    return words;
  }
}
