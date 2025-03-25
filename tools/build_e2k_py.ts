import fs from "node:fs";
import { parseArgs } from "node:util";
import { $, cd } from "zx";

const inferRoot = `${import.meta.dirname}/../infer`;
const wheelsRoot = `${inferRoot}/target/wheels`;

async function main() {
  $.verbose = true;
  cd(`${inferRoot}/crates/e2k-py`);

  const args = processArgs();

  console.log("Replacing version...");
  await replaceVersion(args.version);

  console.log("Building NOTICE.md...");
  await buildNotice();

  if (args.wheel) {
    console.log("Building wheel...");
    await buildWheel();
  }

  if (args.sdist) {
    console.log("Building sdist...");
    await buildSdist();
  }
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});

function processArgs(): {
  wheel: boolean;
  sdist: boolean;
  version: string;
} {
  const args = parseArgs({
    options: {
      wheel: { type: "boolean" },
      sdist: { type: "boolean" },
      version: { type: "string" },
    },
    args: process.argv.slice(2),
  });

  if (!args.values.wheel && !args.values.sdist) {
    throw new Error("Specify at least one of --wheel or --sdist");
  }
  if (!args.values.version) {
    throw new Error("Specify --version");
  }

  return {
    wheel: args.values.wheel ?? false,
    sdist: args.values.sdist ?? false,
    version: args.values.version,
  };
}

async function replaceVersion(version: string) {
  const cargoToml = fs.readFileSync(`${inferRoot}/Cargo.toml`, "utf8");
  let replaced = false;
  const replacedCargoToml = cargoToml.replace(/^version = ".*"$/m, () => {
    replaced = true;
    return `version = "${version}"`;
  });
  if (!replaced) {
    throw new Error("Failed to replace version in Cargo.toml");
  }
  await fs.promises.writeFile(`${inferRoot}/Cargo.toml`, replacedCargoToml);
}

async function buildNotice() {
  await $({
    cwd: `../e2k-rs`,
  })`cargo about generate about.hbs.md`.pipe(fs.createWriteStream(`NOTICE.md`));
}

async function buildWheel() {
  await $`uv run maturin build --release`;

  if (process.platform === "linux") {
    const wheels = await fs.promises.readdir(wheelsRoot);
    const nonManyLinuxWheels = wheels.filter(
      (file) => file.endsWith(".whl") && !file.includes("manylinux"),
    );
    const manyLinuxWheels = wheels.filter(
      (file) => file.endsWith(".whl") && file.includes("manylinux"),
    );
    if (manyLinuxWheels.length !== 1) {
      throw new Error(
        `assert: manyLinuxWheels.length === 1 (${manyLinuxWheels.length})`,
      );
    }
    for (const wheel of nonManyLinuxWheels) {
      await fs.promises.rm(`${wheelsRoot}/${wheel}`);
    }
  }
}

async function buildSdist() {
  // NOTE: maturin sdistのバグでLICENSEが含まれないため、手動で追加する。
  // ref: https://github.com/PyO3/maturin/issues/2531
  const tempDir = await $`mktemp -d -t e2k-py-sdist-XXXXXX`
    .text()
    .then((output) => output.trim());

  await $`uv run maturin sdist -o ${tempDir}`;

  const tarName = await fs.promises.readdir(tempDir).then((files) => files[0]);
  const sdistName = tarName.replace(/\.tar\.gz$/, "");

  await $({ cwd: tempDir })`tar -xzvf ${tarName}`;
  const pkgRoot = `${tempDir}/${sdistName}`;
  await fs.promises.copyFile(
    `${import.meta.dirname}/../LICENSE`,
    `${pkgRoot}/LICENSE`,
  );
  await fs.promises.copyFile(
    `${import.meta.dirname}/../infer/crates/e2k-py/NOTICE.md`,
    `${pkgRoot}/NOTICE.md`,
  );
  await $({ cwd: tempDir })`tar -czvf ${wheelsRoot}/${tarName} ${sdistName}`;
}
