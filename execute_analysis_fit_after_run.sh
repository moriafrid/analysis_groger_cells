#!/bin/bash
# Write output as following (%j is JOB_ID)
#SBATCH -o logs/%j.out
#SBATCH -e logs/%j.err
# Ask for one CPU, one GPU, enter the GPU queue, and limit run to 1 days
#SBATCH -p ss.q
#SBATCH --mem 2000
#SBATCH -c 1
#SBATCH -t 1-0
# check if script is started via SLURM or bash
# if with SLURM: there variable '$SLURM_JOB_ID' will exist
# `if [ -n $SLURM_JOB_ID ]` checks if $SLURM_JOB_ID is not an empty string

echo $#

if [[ $# -ne 5 ]] ; then
    echo "Wrong usage. not have enought parameters"
    exit 1
fi

cell_name=$1
file_type2read=$2
resize_diam_by=$3
shrinkage_factor=$4
folder=$5

shift $#

if [ -n $SLURM_JOB_ID ]; then
  SCRIPT_PATH=$(scontrol show job $SLURM_JOBID | awk -F= '/Command=/{print $2}' | cut -d" " -f1)
else
  SCRIPT_PATH=$(realpath $0) # otherwise: started with bash. Get the real location.
fi

# get script's path to allow running from any folder without errors
path=$(dirname $SCRIPT_PATH)

# If necessary, activate anaconda installed on your user (Default: /ems/..../<lab>/<user>/anaconda3
# source anaconda3/bin/activate
#conda init
#conda activate project
# put your script here - example script is sitting with this bash script

python3 $path/analysis_fit_aftre_run.py $cell_name $file_type2read $resize_diam_by $shrinkage_factor $folder
