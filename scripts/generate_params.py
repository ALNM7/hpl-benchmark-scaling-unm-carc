import argparse
import csv


def factor_pairs(total):
    # all (P, Q) with P*Q == total, from tall (1xN) to square to wide (Nx1)
    return [(p, total // p) for p in range(1, total + 1) if total % p == 0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", nargs="+", type=int, required=True)
    parser.add_argument("--nb", nargs="+", type=int, required=True)
    parser.add_argument("--nodes-min", type=int, required=True)
    parser.add_argument("--nodes-max", type=int, required=True)
    parser.add_argument("--ntasks-per-node", type=int, required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    with open(args.output, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["N", "NB", "P", "Q", "nodes", "ntasks_per_node"])
        for nodes in range(args.nodes_min, args.nodes_max + 1):
            total_ranks = nodes * args.ntasks_per_node
            for p, q in factor_pairs(total_ranks):
                for n in args.n:
                    for nb in args.nb:
                        writer.writerow([n, nb, p, q, nodes, args.ntasks_per_node])


if __name__ == "__main__":
    main()
