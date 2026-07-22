#!/bin/bash
#SBATCH --job-name HPL_ParamSweep
#SBATCH --partition general
#SBATCH --time 00:10:00
#SBATCH --nodes 2
#SBATCH --ntasks-per-node 8
#SBATCH --mem 16GB
#SBATCH --array 1-2

module load gcc/11.2.0-655h hpl

export OMP_PROC_BIND=TRUE
export OMP_PLACES=cores
export OMP_NUM_THREADS=4

PARAMS_FILE=${1:-$SLURM_SUBMIT_DIR/params/HPL_params.csv}
TEMPLATE_FILE=$SLURM_SUBMIT_DIR/scripts/HPL_template.dat
RESULTS_DIR=$SLURM_SUBMIT_DIR/results
RAW_DIR=$RESULTS_DIR/raw
mkdir -p "$RESULTS_DIR" "$RAW_DIR"

PARAMS=$(tail -n +2 "$PARAMS_FILE" | head -n "$SLURM_ARRAY_TASK_ID" | tail -n 1)
N=$(echo "$PARAMS" | awk -F"," '{print $1}')
NB=$(echo "$PARAMS" | awk -F"," '{print $2}')
P=$(echo "$PARAMS" | awk -F"," '{print $3}')
Q=$(echo "$PARAMS" | awk -F"," '{print $4}')

if [ $((P * Q)) -ne "$SLURM_NTASKS" ]; then
    echo "ERROR: P*Q ($((P * Q))) does not match SLURM_NTASKS ($SLURM_NTASKS) for array task $SLURM_ARRAY_TASK_ID" >&2
    exit 1
fi

SCRATCH_DIR=/carc/scratch/users/$USER
TMP_DIR=$(mktemp --directory -p $SCRATCH_DIR)
TMP_WORKING_DIR=$TMP_DIR/$SLURM_ARRAY_TASK_ID
mkdir -p $TMP_WORKING_DIR
cd $TMP_WORKING_DIR

cp $TEMPLATE_FILE $TMP_WORKING_DIR/HPL.dat
sed -i "s/<N>/$N/g; s/<NB>/$NB/g; s/<P>/$P/g; s/<Q>/$Q/g" HPL.dat

srun --mpi=pmi2 xhpl

cp HPL.out "$RAW_DIR/HPL_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.out"

RESULT_HEADER_AND_DATA_LINES=$(grep --after 2 Gflops HPL.out)
RESULT_DATA_LINE=$(echo "$RESULT_HEADER_AND_DATA_LINES" | tail -n 1)
GFLOPS=$(echo "$RESULT_DATA_LINE" | awk -F" " '{print $NF}')

echo "$N,$NB,$P,$Q,$SLURM_JOB_NUM_NODES,$SLURM_NTASKS_PER_NODE,$GFLOPS" > "$RESULTS_DIR/result_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.csv"

cd $SLURM_SUBMIT_DIR
rm -r $TMP_DIR
