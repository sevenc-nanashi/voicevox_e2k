"""
kanalizer-pyをビルドする。

環境構築を済ませた状態でこのファイルを実行するとビルドが行われる想定。
環境構築やレジストリへの公開はこのファイルでは行わない。
"""

import argparse
import os
from pathlib import Path
import platform
import shutil
from subprocess import check_output, run
import tempfile
from common import infer_root, is_windows, is_linux

kanalizer_py_root = infer_root / "crates" / "kanalizer-py"
wheels_root = infer_root / "target" / "wheels"


def main():
    os.chdir(kanalizer_py_root)

    args = process_args()
    wheel: bool = args.wheel
    wheel_on_docker: bool = args.wheel_on_docker
    sdist: bool = args.sdist
    skip_notice: bool = args.skip_notice

    if not skip_notice:
        print("Building NOTICE.md...")
        build_notice()

    if wheel:
        print("Building wheel...")
        build_wheel()
        if is_windows:
            print("Building 32-bit wheel...")
            build_wheel(target="i686-pc-windows-msvc", python_arch="x86")
        elif is_linux:
            print("Removing non-manylinux wheels...")
            remove_non_manylinux_wheels()

    if wheel_on_docker:
        print("Building wheel on docker...")
        build_wheel_on_docker()

    if sdist:
        print("Building sdist...")
        build_sdist()


def process_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--wheel", action="store_true", help="Build wheel")
    parser.add_argument(
        "--wheel-on-docker",
        action="store_true",
        help="Build wheel on docker (Linux only, requires Docker and sudo)",
    )
    parser.add_argument("--sdist", action="store_true", help="Build sdist")
    parser.add_argument(
        "--skip-notice", action="store_true", help="Skip NOTICE.md generation"
    )
    args = parser.parse_args()
    if not any([args.wheel, args.wheel_on_docker, args.sdist]):
        parser.error("Specify at least one of --wheel, --wheel-on-docker or --sdist")
    return args


def build_notice():
    print_and_run(
        [
            "cargo",
            "about",
            "generate",
            "-c",
            infer_root / "tools" / "about.toml",
            infer_root / "tools" / "about.hbs.md",
            "-o",
            kanalizer_py_root / "NOTICE.md",
        ],
        cwd=kanalizer_py_root,
    )


def build_wheel(*, python_arch: str | None = None, target: str | None = None):
    target_args = []
    if target is not None:
        target_args = ["--target", target]
    python_arch_args = []
    if python_arch is not None:
        os_name = {
            "Windows": "windows",
            "Linux": "linux",
            "Darwin": "macos",
        }[platform.system()]
        python_arch_args = [
            "--python",
            f"cpython-{platform.python_version()}-{os_name}-{python_arch}",
        ]
    print_and_run(
        ["uv", "run", *python_arch_args, "maturin", "build", "--release", *target_args]
    )


def remove_non_manylinux_wheels():
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


def build_wheel_on_docker():
    if not is_linux:
        raise Exception("This command must be run on Linux")

    tag = "x86_64" if platform.machine() == "x86_64" else "aarch64"

    os.makedirs(wheels_root, exist_ok=True)
    vars = {
        "DOCKER": "true",
        "HOST_UID": str(os.getuid()),
        "HOST_GID": str(os.getgid()),
    }
    vars_shell = " ".join([f"{k}={v}" for k, v in vars.items()])
    print_and_run(
        [
            "docker",
            "run",
            "--rm",
            "--mount",
            f"type=bind,source={infer_root},target=/mnt/infer",
            f"messense/manylinux_2_28-cross:{tag}",
            "bash",
            "-c",
            f"{vars_shell} bash < /mnt/infer/tools/build_kanalizer_py_docker.sh",
        ]
    )


def build_sdist():
    # NOTE: maturin sdistは特定条件下でLICENSEをsdistに含めないバグがあるため、手動で追加する。
    # ref: https://github.com/PyO3/maturin/issues/2531

    temp_dir = Path(tempfile.mkdtemp(prefix="kanalizer-py-sdist-"))

    print_and_run(["uv", "run", "maturin", "sdist", "-o", temp_dir])

    tar_path = next(temp_dir.glob("*.tar.gz"))
    tar_name = tar_path.name
    sdist_name = tar_name.replace(".tar.gz", "")

    print_and_run(["tar", "-xzvf", tar_name], cwd=temp_dir)
    pkg_root = temp_dir / sdist_name
    shutil.copyfile(kanalizer_py_root / "LICENSE", pkg_root / "LICENSE")
    shutil.copyfile(kanalizer_py_root / "NOTICE.md", pkg_root / "NOTICE.md")

    print_and_run(["tar", "-czvf", wheels_root / tar_name, sdist_name], cwd=temp_dir)


def print_and_run(*args, **kwargs):
    print(f"$ {' '.join(map(str, args[0]))}")
    run(*args, **kwargs, check=True)


def print_and_check_output(*args, **kwargs) -> bytes:
    print(f"$ {' '.join(map(str, args[0]))}")
    return check_output(*args, **kwargs)


if __name__ == "__main__":
    main()
