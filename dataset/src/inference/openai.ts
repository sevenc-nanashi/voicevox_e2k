import { OpenAI as OpenAIClient } from "openai";
import type { Config } from "../config.ts";
import { InferenceProvider } from "./index.ts";

type OpenRouterError = {
  code: string;
  message: string;
};

export class OpenAiInferenceProvider extends InferenceProvider {
  declare config: Config & { inference: { openai: object } };
  client: OpenAIClient;

  constructor(config: Config) {
    if (config.inference.openai == null) {
      throw new Error("OpenAI config is missing");
    }
    super(config);

    this.client = new OpenAIClient({
      baseURL: config.inference.openai.apiBaseUrl,
      apiKey: config.inference.openai.apiKey,
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

    const completion = await this.client.chat.completions.create({
      model: this.config.inference.openai.modelName,

      messages: [{ role: "user", content: prompt }],
    });
    // @ts-expect-error: OpenRouter独自のエラー型。OpenAIのクライアントには型が無いので、ここで型を付ける。
    const maybeError: OpenRouterError | undefined = completion.error;
    if (maybeError != null) {
      throw new Error(`${maybeError.code}: ${maybeError.message}`);
    }
    const response = completion.choices[0].message.content;
    if (response == null) {
      throw new Error("No response");
    }
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
