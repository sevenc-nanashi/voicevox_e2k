import argparse
import os
from subprocess import check_output
import re
import shutil
import tempfile
import platform
from pathlib import Path

infer_root = Path(__file__).parent.parent
e2k_py_root = infer_root / "crates" / "e2k-py"
wheels_root = infer_root / "target" / "wheels"


def main():
    os.chdir(e2k_py_root)

    args = process_args()
    wheel: bool = args.wheel
    sdist: bool = args.sdist
    version: str = args.version

    print("Replacing version...")
    replace_version(infer_root, version)

    print("Building NOTICE.md...")
    build_notice()

    if wheel:
        print("Building wheel...")
        build_wheel()

    if sdist:
        print("Building sdist...")
        build_sdist()


def process_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--wheel", action="store_true", help="Build wheel")
    parser.add_argument("--sdist", action="store_true", help="Build sdist")
    parser.add_argument("--version", type=str, required=True, help="Version to set")
    args = parser.parse_args()
    if not args.wheel and not args.sdist:
        parser.error("Specify at least one of --wheel or --sdist")
    return args


def replace_version(infer_root: Path, version):
    cargo_toml_path = infer_root / "Cargo.toml"
    cargo_toml = cargo_toml_path.read_text(encoding="utf8")
    new_cargo_toml, count = re.subn(
        r'^version = ".*"$', f'version = "{version}"', cargo_toml, flags=re.MULTILINE
    )
    if count == 0:
        raise Exception("Failed to replace version in Cargo.toml")
    cargo_toml_path.write_text(new_cargo_toml, encoding="utf8")


def build_notice():
    result = check_output(
        [
            "cargo",
            "about",
            "generate",
            "-c",
            "../e2k-rs/about.toml",
            "../e2k-rs/about.hbs.md",
        ],
        cwd=e2k_py_root,
    )
    Path("NOTICE.md").write_bytes(result)


def build_wheel():
    check_output(["uv", "run", "maturin", "build", "--release"])
    if platform.system().lower() == "windows":
        check_output(
            [
                "uv",
                "run",
                "-p",
                f"cpython-{platform.python_version()}-windows-x86",
                "maturin",
                "build",
                "--release",
                "--target",
                "i686-pc-windows-msvc",
            ]
        )
    elif platform.system().lower() == "linux":
        wheels = list(wheels_root.iterdir())
        non_manylinux_wheels = [
            f for f in wheels if f.name.endswith(".whl") and "manylinux" not in f.name
        ]
        manylinux_wheels = [
            f for f in wheels if f.name.endswith(".whl") and "manylinux" in f.name
        ]
        if len(manylinux_wheels) != 1:
            raise Exception(
                f"assert: manylinux_wheels.length == 1 ({len(manylinux_wheels)})"
            )
        for wheel in non_manylinux_wheels:
            wheel.unlink()


def build_sdist():
    # NOTE: maturin sdistは特定条件下でLICENSEをsdistに含めないバグがあるため、手動で追加する。
    # ref: https://github.com/PyO3/maturin/issues/2531

    temp_dir = Path(tempfile.mkdtemp(prefix="e2k-py-sdist-"))

    check_output(["uv", "run", "maturin", "sdist", "-o", temp_dir])

    tar_path = next(temp_dir.glob("*.tar.gz"))
    tar_name = tar_path.name
    sdist_name = tar_name.replace(".tar.gz", "")

    check_output(["tar", "-xzvf", tar_name], cwd=temp_dir)
    pkg_root = temp_dir / sdist_name
    shutil.copyfile(e2k_py_root / "LICENSE", pkg_root / "LICENSE")
    shutil.copyfile(e2k_py_root / "NOTICE.md", pkg_root / "NOTICE.md")

    check_output(["tar", "-czvf", wheels_root / tar_name, sdist_name], cwd=temp_dir)


if __name__ == "__main__":
    main()
