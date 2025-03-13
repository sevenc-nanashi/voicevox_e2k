import fs from "node:fs/promises";
import { dump as dumpYaml } from "js-yaml";
import { zodToJsonSchema } from "zod-to-json-schema";
import { configSchema } from "../config.ts";

async function main() {
  const jsonSchema = zodToJsonSchema(configSchema);
  const path = `${import.meta.dirname}/../../config.schema.yml`;
  await fs.writeFile(
    path,
    [
      "# pnpm run tools:generateConfigSchema で生成。手動で編集しないでください。",
      dumpYaml(jsonSchema),
    ].join("\n"),
  );
}

main().catch((err) => {
  console.error(String(err));
  process.exit(1);
});
