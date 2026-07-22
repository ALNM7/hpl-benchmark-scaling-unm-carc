#!/bin/bash
# sbatch cannot change --nodes from inside a running job, so this wrapper
# submits one job per node count with its own params CSV and array size.
set -euo pipefail

NODE_MIN=2
NODE_MAX=6
NTASKS_PER_NODE=8
N_VALUES="60992"
NB_VALUES="64 96 128 160 192 224 256 288"

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO_DIR=$(dirname "$SCRIPT_DIR")
PARAMS_DIR=$REPO_DIR/params

mkdir -p "$PARAMS_DIR"

for nodes in $(seq $NODE_MIN $NODE_MAX); do
    params_file=$PARAMS_DIR/HPL_params_nodes${nodes}.csv

    python3 "$SCRIPT_DIR/generate_params.py" \
        --n $N_VALUES \
        --nb $NB_VALUES \
        --nodes-min $nodes \
        --nodes-max $nodes \
        --ntasks-per-node $NTASKS_PER_NODE \
        --output "$params_file"

    lines=$(($(wc -l < "$params_file") - 1))
    if [ "$lines" -lt 1 ]; then
        echo "No valid P x Q combinations for $nodes nodes, skipping" >&2
        continue
    fi

    sbatch --nodes=$nodes --ntasks-per-node=$NTASKS_PER_NODE --array=1-$lines \
        "$SCRIPT_DIR/hpl_sweep.sbatch" "$params_file"
done
