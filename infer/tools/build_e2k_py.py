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
    wheel_on_docker: bool = args.wheel_on_docker
    sdist: bool = args.sdist
    version: str = args.version
    skip_notice: bool = args.skip_notice

    print("Replacing version...")
    original_version = replace_version(version)

    try:
        if not skip_notice:
            print("Building NOTICE.md...")
            build_notice()

        if wheel:
            print("Building wheel...")
            build_wheel()

        if wheel_on_docker:
            print("Building wheel on docker...")
            build_wheel_on_docker(version)

        if sdist:
            print("Building sdist...")
            build_sdist()
    finally:
        print("Restoring version...")
        replace_version(original_version)


def process_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--wheel", action="store_true", help="Build wheel")
    parser.add_argument(
        "--wheel-on-docker", action="store_true", help="Build wheel on docker"
    )
    parser.add_argument("--sdist", action="store_true", help="Build sdist")
    parser.add_argument("--version", type=str, required=True, help="Version to set")
    parser.add_argument("--skip-notice", action="store_true", help="Skip NOTICE.md generation")
    args = parser.parse_args()
    if not any([args.wheel, args.wheel_on_docker, args.sdist]):
        parser.error("Specify at least one of --wheel, --wheel-on-docker or --sdist")
    return args


def replace_version(version: str) -> str:
    cargo_toml_path = infer_root / "Cargo.toml"
    cargo_toml = cargo_toml_path.read_text(encoding="utf8")
    version_pattern = re.compile(r'^version = "(.*)"$', flags=re.MULTILINE)
    match = version_pattern.search(cargo_toml)
    if match is None:
        raise Exception("Failed to find version in Cargo.toml")
    original_version = match.group(1)
    new_cargo_toml = version_pattern.sub(f'version = "{version}"', cargo_toml)
    cargo_toml_path.write_text(new_cargo_toml, encoding="utf8")
    return original_version


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


def build_wheel_on_docker(version: str):
    if platform.system().lower() != "linux":
        raise Exception("This command must be run on Linux")

    tag = "x86_64" if platform.machine() == "x86_64" else "aarch64"

    check_output(
        [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{infer_root}:/mnt",
            f"messense/manylinux_2_28-cross:{tag}",
            "bash",
            "-c",
            " && ".join(
                [
                    "(curl -LsSf https://astral.sh/uv/install.sh | sh)",
                    "(curl -LsSf https://sh.rustup.rs | sh -s -- -y --profile minimal)",
                    "export PATH=$HOME/.cargo/bin:$HOME/.local/bin:$PATH",
                    "cd /mnt/tools",
                    f"uv run ./build_e2k_py.py --wheel --version {version} --skip-notice",
                ]
            ),
        ]
    )


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
