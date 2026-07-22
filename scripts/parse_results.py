import argparse
import csv
import glob
import re

# HPL result lines look like: WR11C2R4   60992   128   4   8   73.16   2.2887e+03
LINE_RE = re.compile(
    r"^(?P<test>\S+)\s+(?P<n>\d+)\s+(?P<nb>\d+)\s+(?P<p>\d+)\s+(?P<q>\d+)\s+"
    r"(?P<time>[\d.]+)\s+(?P<gflops>[\d.eE+-]+)\s*$"
)


def parse_file(path):
    rows = []
    with open(path) as f:
        for line in f:
            m = LINE_RE.match(line.strip())
            if m:
                rows.append({
                    "N": int(m.group("n")),
                    "NB": int(m.group("nb")),
                    "P": int(m.group("p")),
                    "Q": int(m.group("q")),
                    "time_s": float(m.group("time")),
                    "GFLOPS": float(m.group("gflops")),
                    "source_file": path,
                })
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-dir", default="results/raw")
    parser.add_argument("--output", default="results/parsed_results.csv")
    args = parser.parse_args()

    all_rows = []
    for path in sorted(glob.glob(f"{args.raw_dir}/*.out")):
        all_rows.extend(parse_file(path))

    with open(args.output, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["N", "NB", "P", "Q", "time_s", "GFLOPS", "source_file"])
        writer.writeheader()
        writer.writerows(all_rows)


if __name__ == "__main__":
    main()
