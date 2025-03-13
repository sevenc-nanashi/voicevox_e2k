import * as z from "zod";

export const configSchema = z.object({
  randomSeed: z.string(),
  source: z.object({
    provider: z.enum(["cmudict"]),
    maxNumWords: z.union([z.number(), z.literal("all")]),
  }),
  inference: z.object({
    provider: z.enum(["gemini"]),
    concurrency: z.number(),

    gemini: z.object({
      apiKey: z.string(),
      modelName: z.string(),
    }),
  }),
});

export type Config = z.infer<typeof configSchema>;
