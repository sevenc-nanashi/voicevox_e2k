import {
  type GenerativeModel,
  GoogleGenerativeAI,
} from "@google/generative-ai";
import type { Config } from "../config.ts";
import { InferenceProvider } from "./index.ts";

export class GeminiInferenceProvider extends InferenceProvider {
  declare config: Config & { inference: { gemini: object } };
  genAI: GoogleGenerativeAI;
  model: GenerativeModel;

  constructor(config: Config) {
    if (config.inference.gemini == null) {
      throw new Error("Gemini config is missing");
    }
    super(config);

    this.genAI = new GoogleGenerativeAI(config.inference.gemini.apiKey);
    this.model = this.genAI.getGenerativeModel({
      model: config.inference.gemini.modelName,
    });
  }

  async infer(words: string[]) {
    const prompt = [
      "以下の単語の日本語風の発音を推定し、指定された形式で出力してください。",
      "他のテキストは含めないでください。",
      "文字の名前で読むことは強く禁止されています（例：'ai'は'エーアイ'ではなく'アイ'です）。",
      "単語:",
      ...words,
      "形式:",
      "ai=アイ",
      "ui=ウイ",
      "usb=ウスブ",
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
