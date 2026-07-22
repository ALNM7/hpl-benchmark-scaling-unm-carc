# HPL Benchmark Scaling on the Hopper Cluster (UNM CARC)

Parameter sweep, output parsing, and scaling analysis for the High Performance
Linpack (HPL) benchmark, run on the Hopper cluster at the University of New
Mexico Center for Advanced Research Computing (CARC).

This repository is the tooling and results for my individual contribution
(Hopper) to a three-person HPL benchmarking project across three UNM CARC
clusters. The full write-up, including the Easley and class cluster sections
covered by my teammates, is in `HPC_HPL.pdf`.

## What HPL measures

HPL solves a large dense system of linear equations Ax = b using LU
decomposition with partial pivoting, distributed across MPI ranks. It reports
the achieved floating point rate in GFLOP/s and is the benchmark used to rank
systems on the TOP500 list. Its performance depends heavily on three
parameters:

- **N**: the matrix size (problem size)
- **NB**: the block size used to tile the matrix for the distributed
  factorization
- **P x Q**: the shape of the MPI process grid, where P * Q equals the total
  number of MPI ranks

## Compute environment

- Cluster: Hopper (UNM CARC)
- 32 cores per node
- InfiniBand interconnect
- Compiler: GCC
- Scheduler: Slurm

## Methodology

N was chosen as roughly 80% of the available RAM for a given rank count, to
maximize problem size without running out of memory. NB was swept over
64, 96, 128, 160, 192, 224, 256, and 288. Process grid shapes were swept
across all valid P x Q factorizations of the rank count, from tall (e.g.
2x16) to square (e.g. 8x8) to wide (e.g. 32x1), to isolate the effect of
grid shape on communication cost.

Two scaling regimes were studied:

- **Strong scaling (Amdahl's Law)**: problem size N held fixed while the
  number of MPI ranks increases. Runtime drops as ranks increase, but gains
  diminish as the serial fraction and communication overhead start to
  dominate.
- **Weak scaling (Gustafson's Law)**: N grows together with the rank count
  so that the work per rank stays roughly constant. Runtime grows with N,
  but the achieved GFLOP/s stays stable if communication overhead doesn't
  grow faster than the added compute.

`scripts/submit_sweep.sh` automates submission across node counts from 2 to
6, generating a separate parameter file and Slurm array for each node count
since `--nodes` cannot be changed once a job is running.

## Repository layout

```
scripts/
  HPL_template.dat      HPL.dat template with <N>, <NB>, <P>, <Q> placeholders
  hpl_sweep.sbatch       Slurm array job, one HPL run per array task
  aggregate_results.sh   combines per-task result files into one CSV
  submit_sweep.sh        wrapper that submits one sbatch job per node count (2-6)
  generate_params.py     generates the parameter CSV (N, NB, P, Q, nodes, ntasks_per_node)
  parse_results.py       parses HPL .out files into a consolidated CSV
params/                  generated parameter CSVs (one per node count)
results/                 per-task result CSVs, raw HPL .out files, consolidated CSVs
analysis/
  analyze_scaling.py     speedup, efficiency, and plots
requirements.txt
HPC_HPL.pdf              full project report (all three clusters)
```

## Running the sweep

1. Generate a parameter file (or let `submit_sweep.sh` do this per node
   count):

   ```
   python3 scripts/generate_params.py \
     --n 60992 \
     --nb 64 96 128 160 192 224 256 288 \
     --nodes-min 2 --nodes-max 6 \
     --ntasks-per-node 8 \
     --output params/HPL_params.csv
   ```

2. Submit the full sweep across node counts 2 to 6:

   ```
   bash scripts/submit_sweep.sh
   ```

   Each node count gets its own parameter CSV under `params/` and its own
   `sbatch --array` job, sized to the number of valid P x Q combinations for
   that rank count.

3. Once jobs finish, combine the quick per-task GFLOPS files into one CSV:

   ```
   bash scripts/aggregate_results.sh results results/HPL_results.csv
   ```

4. Parse the raw HPL `.out` files (preserved under `results/raw/`) into a
   consolidated CSV with runtime and GFLOP/s:

   ```
   python3 scripts/parse_results.py --raw-dir results/raw --output results/parsed_results.csv
   ```

5. Generate plots:

   ```
   python3 analysis/analyze_scaling.py --input results/parsed_results.csv nb-sweep --n 60992 --p 4 --q 8
   python3 analysis/analyze_scaling.py --input results/parsed_results.csv grid-shape --n 60992 --nb 128
   python3 analysis/analyze_scaling.py --input results/parsed_results.csv strong-scaling --n 60992 --nb 160
   python3 analysis/analyze_scaling.py --input results/parsed_results.csv weak-scaling --p 8 --q 8 --nb 160
   ```

## Results

### Block size sweep (N=60992, P x Q=4x8, 32 ranks)

| NB | GFLOP/s |
|----|---------|
| 64 | ~746 |
| 96-128 | ~935-950 (peak) |
| 192 | ~765 |
| 256-288 | below 300 |

Medium block sizes give the best balance between computation and
communication; very large blocks collapse performance.

### Process grid shape (N=60992, NB=128, 32 ranks)

Grids tested: 2x16, 4x8, 8x4, 16x2, 32x1.

| Grid | GFLOP/s |
|------|---------|
| 2x16 | ~209 (worst) |
| 8x4 | ~1106 (best) |

The near-square 8x4 grid clearly outperforms the elongated 2x16 grid.

### Larger problems

- N=86242, P x Q=8x8 (64 ranks): best at NB=160, ~1.83 TFLOP/s
- N=121984, P x Q=16x8 (128 ranks): best at NB=160-192, ~2.67 TFLOP/s

### Weak scaling (P x Q=8x8, NB=160)

N was increased from 86242 to 90000 to 100242. Runtime grew from about
232-234 s at N=86242 to about 390 s at N=100242, while performance stayed
stable in the 1.7-1.8 TFLOP/s range across all three points.

As N grows, runtime increases but the achieved GFLOP/s stays stable, in
line with Gustafson's Law.

### Best run per rank count

| Ranks | N | Best performance |
|-------|-----|-------------------|
| 32 | 60992 | ~1.11 TFLOP/s |
| 64 | 86242 | ~1.84 TFLOP/s |
| 128 | 121984 | ~2.95 TFLOP/s |

Larger problems with more ranks reach higher absolute performance, but only
with the right NB and grid shape.

## Authors

This work is part of a three-person HPL benchmarking project at UNM. The
Hopper cluster (this repository) was my individual contribution.

- **Alfredo Navarrete Montes** (Hopper cluster)
- Yun Zheng (class cluster)
- Evelyn Sanchez (Easley cluster)

See `HPC_HPL.pdf` for the full report.
