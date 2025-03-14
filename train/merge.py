import json
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("--output", type=str, required=True)
parser.add_argument("files", nargs="+")
args = parser.parse_args()

merged = {}
for file in args.files:
    with open(file, "r") as f:
        for line in tqdm(f, desc=f"Processing {file}"):
            if not line:
                continue
            line_data = json.loads(line)
            if line_data["word"] in merged:
                merged[line_data["word"]].extend(line_data["kata"])
            else:
                merged[line_data["word"]] = line_data["kata"]

with open(args.output, "w") as f:
    for word, kata in tqdm(merged.items(), desc="Writing"):
        f.write(json.dumps({"word": word, "kata": kata}, ensure_ascii=False) + "\n")
