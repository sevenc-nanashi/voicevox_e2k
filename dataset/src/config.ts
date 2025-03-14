import * as z from "zod";

export const configSchema = z.object({
  randomSeed: z.number(),
  source: z.object({
    provider: z.enum(["cmudict"]),
    maxNumWords: z.union([z.number(), z.literal("all")]),
  }),
  inference: z.object({
    provider: z.enum(["gemini", "openai"]),
    concurrency: z.number(),

    gemini: z.object({
      apiKey: z.string(),
      modelName: z.string(),
    }),
    openai: z.object({
      apiBaseUrl: z.string(),
      apiKey: z.string(),
      modelName: z.string(),
    }),
  }),
});

export type Config = z.infer<typeof configSchema>;
