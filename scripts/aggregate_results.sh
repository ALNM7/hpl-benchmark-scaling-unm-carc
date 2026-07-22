#!/bin/bash
# Combines the per-task result files written by hpl_sweep.sbatch into one CSV.
# Per-task files avoid concurrent array tasks interleaving lines in a shared file.

RESULTS_DIR=${1:-results}
OUTPUT_FILE=${2:-$RESULTS_DIR/HPL_results.csv}

echo "N,NB,P,Q,nodes,ntasks_per_node,GFLOPS" > "$OUTPUT_FILE"

for f in "$RESULTS_DIR"/result_*.csv; do
    [ -e "$f" ] || continue
    cat "$f" >> "$OUTPUT_FILE"
done
