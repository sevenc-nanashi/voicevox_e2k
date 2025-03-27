import argparse
import re
from paths import infer_root


def main():
    args = process_args()
    version = args.version
    print("Replacing version...")
    old_version = replace_version(version)
    print(f"Replaced version from {old_version} to {version}")


def process_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version",
        type=str,
        required=True,
        help="Version to replace in Cargo.toml",
    )
    args = parser.parse_args()
    return args


def replace_version(version: str) -> str:
    cargo_toml_path = infer_root / "Cargo.toml"
    cargo_toml = cargo_toml_path.read_text(encoding="utf8")
    version_pattern = re.compile(r'^version = "(.*)"$', flags=re.MULTILINE)
    match = version_pattern.search(cargo_toml)
    if match is None:
        raise Exception("Failed to find version in Cargo.toml")
    old_version = match.group(1)
    new_cargo_toml = version_pattern.sub(f'version = "{version}"', cargo_toml)
    cargo_toml_path.write_text(new_cargo_toml, encoding="utf8")
    return old_version


if __name__ == "__main__":
    main()
