#!/bin/bash
# Write output as following (%j is JOB_ID)
#SBATCH -o logs/%j.out
#SBATCH -e logs/%j.err
# Ask for one CPU, one GPU, enter the GPU queue, and limit run to 1 days
#SBATCH -p ss.q
#SBATCH --mem 2000
#SBATCH -c 1
#SBATCH -t 1-0
echo $#

if [[ $# -ne 6 ]] ; then
    echo "Wrong usage. not have enought parameters"
    exit 1
fi

cell_name=$1
file_type2read=$2
resize_diam_by=$3
shrinkage_factor=$4
SPINE_START=$5
folder=$6

shift $#
if [ -n $SLURM_JOB_ID ]; then
  # check the original location through scontrol and $SLURM_JOB_ID
  SCRIPT_PATH=$(scontrol show job $SLURM_JOBID | awk -F= '/Command=/{print $2}' | cut -d" " -f1)
else
  # otherwise: started with bash. Get the real location.
  SCRIPT_PATH=$(realpath $0)
fi

path=$(dirname $SCRIPT_PATH) # get script's path to allow running from any folder without errors

python3 $path/best_with_const_param.py $cell_name $file_type2read $resize_diam_by $shrinkage_factor $SPINE_START $folder
