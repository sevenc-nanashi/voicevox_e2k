import * as z from "zod";

export const configSchema = z.object({
  randomSeed: z.number(),
  source: z.object({
    provider: z.enum(["cmudict"]),
    maxNumWords: z.union([z.number(), z.literal("all")]),
  }),
  inference: z.object({
    provider: z.enum(["gemini", "openai", "dummy"]),
    concurrency: z.number(),
    rateLimit: z.object({
      waitMs: z.number(),
      maxRetries: z.number(),
      throttleMs: z.number(),
    }),

    batch: z.union([
      z.object({
        type: z.literal("fixed"),
        batchSize: z.number(),
      }),
      z.object({
        type: z.literal("bisect"),
        maxBatchSize: z.number(),
        ratio: z.number(),
      }),
    ]),

    gemini: z
      .object({
        apiKey: z.string(),
        modelName: z.string(),
      })
      .optional(),
    openai: z
      .object({
        apiBaseUrl: z.string(),
        apiKey: z.string(),
        modelName: z.string(),
      })
      .optional(),
  }),
});

export type Config = z.infer<typeof configSchema>;
