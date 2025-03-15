import os
from e2k import constants
import subprocess


destination = os.path.join(os.path.dirname(__file__), "../src/constants.rs")
content = f"""
// `task generate_constants` により生成。
// このファイルは直接編集しないでください。

// pub const PAD_IDX: usize = {constants.PAD_IDX};
pub const SOS_IDX: usize = {constants.SOS_IDX};
pub const EOS_IDX: usize = {constants.EOS_IDX};
pub const KANAS: &[&str] = &[
{", ".join([f'"{kana}"' for kana in constants.kanas])}
];
pub const ASCII_ENTRIES: &[&str] = &[
{", ".join([f'"{entry}"' for entry in constants.ascii_entries])}
];
"""

formatted_content = subprocess.run(
    ["rustfmt", "--edition", "2021"],
    input=content.encode(),
    stdout=subprocess.PIPE,
).stdout.decode()
with open(destination, "w") as f:
    f.write(formatted_content)
