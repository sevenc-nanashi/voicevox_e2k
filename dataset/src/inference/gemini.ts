import {
  type GenerativeModel,
  GoogleGenerativeAI,
} from "@google/generative-ai";
import type { InferenceProvider } from "./index.ts";
import { config } from "../config.ts";

export class Gemini implements InferenceProvider {
  genAI: GoogleGenerativeAI;
  model: GenerativeModel;
  constructor() {
    this.genAI = new GoogleGenerativeAI(config.gemini.apiKey);
    this.model = this.genAI.getGenerativeModel({
      model: config.gemini.modelName,
    });
  }

  async infer(words: string[]) {
    const prompt = [
      "Estimate Japanese-style pronunciation of these words, and output in the specified format. Don't include any other texts.",
      "Words:",
      ...words,
      "Format:",
      "word=ワード",
      "helmet=ヘルメット",
    ].join("\n");

    const response = await this.model
      .generateContent(prompt)
      .then((res) => res.response.text());
    const resultPattern = /^([a-z]+)=(.+)$/gm;
    const results = Object.fromEntries(
      [...response.matchAll(resultPattern)].map((match) => [
        match[1],
        match[2],
      ]),
    );

    return results;
  }
}
