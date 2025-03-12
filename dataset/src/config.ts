import * as fs from "node:fs/promises";
import * as z from "zod";
import { load as loadYaml } from "js-yaml";

const configSchema = z.object({
  gemini: z.object({
    apiKey: z.string(),
    modelName: z.string(),
  }),
});

export type Config = z.infer<typeof configSchema>;

export const config = configSchema.parse(
  loadYaml(await fs.readFile(`${import.meta.dirname}/../config.yml`, "utf-8")),
);
