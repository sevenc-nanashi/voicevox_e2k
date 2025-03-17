import fs from "node:fs/promises";
import { dump as dumpYaml } from "js-yaml";
import { zodToJsonSchema } from "zod-to-json-schema";
import { configSchema } from "../config.ts";

async function main() {
  const isCheck = process.argv.includes("--check");

  const jsonSchema = zodToJsonSchema(configSchema);
  const path = `${import.meta.dirname}/../../config.schema.yml`;
  const content = [
    "# pnpm run tools:generateConfigSchema で生成。手動で編集しないでください。",
    dumpYaml(jsonSchema),
  ].join("\n");

  if (isCheck) {
    await checkConfigSchema(path, content);
  } else {
    await writeConfigSchema(path, content);
  }
}

async function checkConfigSchema(path: string, content: string): Promise<void> {
  const currentContent = await fs.readFile(path, "utf-8");
  if (currentContent !== content) {
    console.error(
      `Config schema is out of date. Run 'pnpm run tools:generateConfigSchema' to update it.`,
    );
    process.exit(1);
  }
  console.log("Config schema is up to date.");
}

async function writeConfigSchema(path: string, content: string): Promise<void> {
  await fs.writeFile(path, content);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
