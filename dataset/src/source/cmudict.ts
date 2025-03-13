import fs from "node:fs/promises";
import { SourceProvider } from "./index.ts";

export class CmuDict extends SourceProvider {
  async getWords() {
    const dictPath = `${import.meta.dirname}/../../deps/cmudict/cmudict-0.7b`;
    const dictContent = await fs.readFile(dictPath, "utf-8");
    const dictPattern = /^([A-Z]{3,}) {2}.+$/gm;

    const words = dictContent.matchAll(dictPattern);

    return Array.from(words, (match) => match[1].toLowerCase());
  }
}
