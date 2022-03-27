#!/bin/bash
# run with: sbatch ./execute_python_script.sh calculate_synaptic_loc.py 1 2 3 hi 3

# Write output as following (%j is JOB_ID)
#SBATCH -o logs/%j.out
#SBATCH -e logs/%j.err
# Ask for one CPU, one GPU, enter the GPU queue, and limit run to 1 days
#SBATCH -p ss.q,elsc.q
#SBATCH --mem 4GB
##SBATCH -c 1
##SBATCH -t 1-0
#SBATCH --exclude=ielsc-48,ielsc-49,ielsc-44,ielsc-45,,ielsc-46,ielsc-42

echo "the number parameters the sbatch get is "$#

args=""
if [[ $# -lt 1 ]] ; then
    echo "Wrong usage. not have enought parameters (must receive script)"
    exit 1
fi

args=$@
shift $#

# `if [ -n $SLURM_JOB_ID ]` checks if $SLURM_JOB_ID is not an empty string
if [ -n "$SLURM_JOB_ID" ]; then
# check the original location through scontrol and $SLURM_JOB_ID
   SCRIPT_PATH=$(scontrol show job $SLURM_JOBID | awk -F= '/Command=/{print $2}' | cut -d" " -f1)
   echo "Got $SLURM_JOB_ID. Using $SCRIPT_PATH"
else
# otherwise: started with bash. Get the real location.
   SCRIPT_PATH=$(realpath $0)
   echo "hi" $SCRIPT_PATH
fi

path=$(dirname $SCRIPT_PATH)
echo "Running: python3 $path/$script $args"
python3 $path/$fit_best_with_const_param.py $args
