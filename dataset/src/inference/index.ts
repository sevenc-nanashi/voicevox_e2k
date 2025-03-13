import type { Config } from "../config.ts";

export abstract class InferenceProvider {
  config: Config;

  constructor(config: Config) {
    this.config = config;
  }
  abstract infer(words: string[]): Promise<Record<string, string>>;
}

export { Gemini } from "./gemini.ts";
