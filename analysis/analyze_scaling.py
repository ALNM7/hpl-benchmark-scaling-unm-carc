import argparse

import matplotlib.pyplot as plt
import pandas as pd


def load(path):
    df = pd.read_csv(path)
    df["ranks"] = df["P"] * df["Q"]
    return df


def nb_sweep(df, n, p, q, output):
    subset = df[(df["N"] == n) & (df["P"] == p) & (df["Q"] == q)].sort_values("NB")
    plt.figure()
    plt.plot(subset["NB"], subset["GFLOPS"], marker="o")
    plt.xlabel("Block size NB")
    plt.ylabel("GFLOP/s")
    plt.title(f"NB sweep at N={n}, P x Q={p}x{q}")
    plt.tight_layout()
    plt.savefig(output)


def grid_shape(df, n, nb, output):
    subset = df[(df["N"] == n) & (df["NB"] == nb)].sort_values("ranks")
    labels = subset["P"].astype(str) + "x" + subset["Q"].astype(str)
    plt.figure()
    plt.bar(labels, subset["GFLOPS"])
    plt.xlabel("Process grid P x Q")
    plt.ylabel("GFLOP/s")
    plt.title(f"Grid shape effect at N={n}, NB={nb}")
    plt.tight_layout()
    plt.savefig(output)


def strong_scaling(df, n, nb, output_prefix):
    subset = df[(df["N"] == n) & (df["NB"] == nb)]
    best = subset.loc[subset.groupby("ranks")["GFLOPS"].idxmax()].sort_values("ranks")
    base_gflops = best["GFLOPS"].iloc[0]
    base_ranks = best["ranks"].iloc[0]
    speedup = best["GFLOPS"] / base_gflops
    ideal_speedup = best["ranks"] / base_ranks
    efficiency = speedup / ideal_speedup

    plt.figure()
    plt.plot(best["ranks"], speedup, marker="o", label="measured")
    plt.plot(best["ranks"], ideal_speedup, linestyle="--", label="ideal")
    plt.xlabel("MPI ranks")
    plt.ylabel("Speedup")
    plt.title(f"Strong scaling speedup, N={n}")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{output_prefix}_speedup.png")

    plt.figure()
    plt.plot(best["ranks"], efficiency, marker="o")
    plt.xlabel("MPI ranks")
    plt.ylabel("Efficiency")
    plt.title(f"Strong scaling efficiency, N={n}")
    plt.tight_layout()
    plt.savefig(f"{output_prefix}_efficiency.png")


def weak_scaling(df, p, q, nb, output_prefix):
    subset = df[(df["P"] == p) & (df["Q"] == q) & (df["NB"] == nb)].sort_values("N")

    plt.figure()
    plt.plot(subset["N"], subset["time_s"], marker="o")
    plt.xlabel("Matrix size N")
    plt.ylabel("Runtime (s)")
    plt.title(f"Weak scaling runtime, P x Q={p}x{q}, NB={nb}")
    plt.tight_layout()
    plt.savefig(f"{output_prefix}_runtime.png")

    plt.figure()
    plt.plot(subset["N"], subset["GFLOPS"], marker="o")
    plt.xlabel("Matrix size N")
    plt.ylabel("GFLOP/s")
    plt.title(f"Weak scaling performance, P x Q={p}x{q}, NB={nb}")
    plt.tight_layout()
    plt.savefig(f"{output_prefix}_gflops.png")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="results/parsed_results.csv")
    sub = parser.add_subparsers(dest="command", required=True)

    p1 = sub.add_parser("nb-sweep")
    p1.add_argument("--n", type=int, required=True)
    p1.add_argument("--p", type=int, required=True)
    p1.add_argument("--q", type=int, required=True)
    p1.add_argument("--output", default="analysis/nb_sweep.png")

    p2 = sub.add_parser("grid-shape")
    p2.add_argument("--n", type=int, required=True)
    p2.add_argument("--nb", type=int, required=True)
    p2.add_argument("--output", default="analysis/grid_shape.png")

    p3 = sub.add_parser("strong-scaling")
    p3.add_argument("--n", type=int, required=True)
    p3.add_argument("--nb", type=int, required=True)
    p3.add_argument("--output-prefix", default="analysis/strong_scaling")

    p4 = sub.add_parser("weak-scaling")
    p4.add_argument("--p", type=int, required=True)
    p4.add_argument("--q", type=int, required=True)
    p4.add_argument("--nb", type=int, required=True)
    p4.add_argument("--output-prefix", default="analysis/weak_scaling")

    args = parser.parse_args()
    df = load(args.input)

    if args.command == "nb-sweep":
        nb_sweep(df, args.n, args.p, args.q, args.output)
    elif args.command == "grid-shape":
        grid_shape(df, args.n, args.nb, args.output)
    elif args.command == "strong-scaling":
        strong_scaling(df, args.n, args.nb, args.output_prefix)
    elif args.command == "weak-scaling":
        weak_scaling(df, args.p, args.q, args.nb, args.output_prefix)


if __name__ == "__main__":
    main()
