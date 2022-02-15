#!/bin/bash
# Write output as following (%j is JOB_ID)
#SBATCH -o outputs/%j.out
#SBATCH -e errors/%j.err
# Ask for one CPU, one GPU, enter the GPU queue, and limit run to 1 days
#SBATCH -p ss.q
#SBATCH --mem 2000
#SBATCH -c 1
#SBATCH -t 1-0

if [ -n $SLURM_JOB_ID ]; then
  # check the original location through scontrol and $SLURM_JOB_ID
  SCRIPT_PATH=$(scontrol show job $SLURM_JOBID | awk -F= '/Command=/{print $2}' | cut -d" " -f1)
else
  # otherwise: started with bash. Get the real location.
  SCRIPT_PATH=$(realpath $0)
fi

path=$(dirname $SCRIPT_PATH) # get script's path to allow running from any folder without errors

# If necessary, activate anaconda installed on your user (Default: /ems/..../<lab>/<user>/anaconda3
# source anaconda3/bin/activate
# put your script here - example script is sitting with this bash script
python3 $path/find_Rinput.py

python3 $path/best_with_const_param.py
