# High-Performance Linpack (HPL) Benchmark: Optimisation and Scaling Laws

This project evaluates **HPL benchmarking performance** across multiple HPC clusters at the **University of New Mexico (UNM) Center for Advanced Research Computing (CARC)**, focusing on parameter tuning and scaling behavior.

## Highlights
- Parameter sweep over **matrix size (N)**, **block size (NB)**, and **MPI process grid (P×Q)**.
- Automated experiments using **Slurm batch scripts** and CSV-driven configurations.
- Strong scaling (Amdahl’s Law) and weak scaling (Gustafson’s Law) analyses.
- Peak single-node performance on Easley: **3.4521 TFLOPS** with **N=160,000**, **NB=224**, **P×Q=8×8** (64 ranks).

## Clusters Evaluated
- **Class cluster**
- **Hopper** (InfiniBand, 32 cores per node; GCC toolchain)
- **Easley** (Intel Xeon Gold 6438Y+; 64 cores; 251 GB RAM; InfiniBand)

## Method Overview
1. Generate `HPL.dat` from a template using chosen **N**, **NB**, and **P×Q**.
2. Run HPL using Slurm (`srun xhpl`).
3. Parse outputs to extract runtime and performance (GFLOP/s).
4. Plot trends:
   - performance vs NB
   - performance vs grid shape
   - strong scaling speedup/efficiency
   - weak scaling runtime and GFLOP/s stability

## Reproducibility
> Note: exact module names and paths depend on each HPC environment.

### 1) Generate HPL.dat
Use `scripts/gen_hpl_dat.py` to generate `HPL.dat` from `hpl/HPL.dat.template`.

### 2) Run with Slurm job arrays
See `slurm/run_hpl_array.slurm` for a CSV-driven parameter sweep.

### 3) Parse outputs
Use `scripts/parse_hpl_out.py` to extract metrics into CSV.

## Report
The full technical report (PDF) is included in:
- `reports/HPC_Project1_Report_Team6.pdf`

## Authors
ALFREDO NAVARRETE MONTES
YUN ZHENG
EVELYN SANCHEZ
