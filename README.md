# High-Performance Linpack (HPL) Benchmark: Optimisation and Scaling Laws

This project evaluates **High Performance Linpack (HPL) benchmark performance** across multiple HPC clusters at the **University of New Mexico Center for Advanced Research Computing (CARC)**.

The objective was to identify optimal parameter configurations and analyze **scaling behavior of distributed HPC workloads**.

---

# Technologies

- MPI
- HPL Benchmark
- Slurm Workload Manager
- Python (data analysis & plotting)
- Jupyter Notebooks
- HPC Clusters (CARC)

---

# Clusters Evaluated

Experiments were executed on the following UNM HPC systems:

• **Class Cluster**  
• **Hopper Cluster** – InfiniBand network, 32 cores per node  
• **Easley Cluster** – Dual Intel Xeon Gold 6438Y+, 64 cores, 251GB RAM

---

# Experimental Methodology

The benchmark was optimized by exploring different HPL parameters:

- Matrix size **N**
- Block size **NB**
- MPI process grid **P × Q**

Automation was implemented using **Slurm job scripts and parameter sweeps**.

The workflow:

1. Generate `HPL.dat` configuration files
2. Submit jobs through Slurm
3. Execute HPL runs with `srun xhpl`
4. Parse output files to extract performance metrics
5. Analyze results with Python and visualize trends

---

# Results

## Process Grid Optimization

The shape of the MPI process grid significantly affects performance.



For **N = 60992**, **NB = 128**, and **32 ranks**:

| Process Grid | Performance |
|---------------|-------------|
| 2×16 | ~209 GFLOP/s |
| 4×8 | ~960 GFLOP/s |
| **8×4** | **~1106 GFLOP/s (best)** |
| 16×2 | ~930 GFLOP/s |
| 32×1 | ~750 GFLOP/s |

Near-square grids achieve the best communication patterns and significantly outperform elongated grids.

---

## Block Size Optimization

Performance was evaluated for different **block sizes (NB)**.



For **N = 60992**, **P×Q = 4×8**:

| NB | GFLOP/s |
|----|---------|
| 64 | ~746 |
| 96 | ~935 |
| 128 | ~950 |
| 160 | ~840 |
| 192 | ~765 |
| 224 | ~510 |
| 256 | ~270 |

Medium block sizes provide the best balance between communication and computation.

---

## Block Size Optimization for Large Problems



For **N = 121984** and **128 ranks (P×Q = 16×8)**:

| NB | Performance |
|----|-------------|
| 128 | ~2440 GFLOP/s |
| **160** | **~2680 GFLOP/s (best)** |
| 192 | ~2670 GFLOP/s |
| 256 | ~2590 GFLOP/s |

Optimal NB values again lie in the **160–192 range**.

---

## Strong Scaling Results

Strong scaling experiments were conducted on the Team Cluster with **fixed problem size N = 14616**.



| Processes | Runtime (s) | GFLOP/s | Speedup | Efficiency |
|-----------|-------------|---------|---------|-----------|
| 4 | 50.30 | 41.39 | 1.00 | 1.00 |
| 8 | 28.17 | 73.90 | 1.79 | 0.89 |
| 16 | 17.21 | 120.94 | 2.92 | 0.73 |
| 24 | 12.47 | 167.01 | 4.03 | 0.67 |
| 32 | 9.53 | 218.40 | 5.28 | 0.66 |

Runtime decreases as more processes are used, though scaling efficiency gradually decreases due to communication overhead.

---

## Weak Scaling Results

Weak scaling experiments increased matrix size as the number of processors increased.



Runtime grows gradually as the global matrix size increases.

| N | Runtime |
|---|--------|
| 14616 | ~50 s |
| 20670 | ~77 s |
| 29232 | ~134 s |
| 35802 | ~170 s |
| 41340 | ~202 s |

---



Performance increases with larger matrices:

| N | GFLOP/s |
|---|--------|
| 14616 | ~41 |
| 20670 | ~76 |
| 29232 | ~124 |
| 35802 | ~180 |
| 41340 | ~233 |

This behavior follows **Gustafson's Law**, where larger problems allow better hardware utilization.

---

# Key Findings

• **Optimal block size range:** NB ≈ 128–192  
• **Best process grid:** near-square configurations (8×4, 8×8)  
• **Peak Easley performance:** **3.45 TFLOPS**  
• Larger matrices significantly improve computational efficiency.

---

# Full Technical Report

The full research report is included in the repo.


# Authors

**ALFREDO NAVARRETE MONTES**  

**YUN ZHENG**

**EVELYN SANCHEZ** 




