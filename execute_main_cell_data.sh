#!/bin/bash

#pass 1 argument = cell


# Write output as following (%j is JOB_ID)
#SBATCH -o outputs/output-%j.out
#SBATCH -e errors/error-%j.err
#SBATCH --mem 60000
#SBATCH -t 2-0
#SBATCH -c 1


set -x

PWD=$(pwd)
LOGS=$PWD/logs
mkdir -p $LOGS
#
#export PATH="/ems/elsc-labs/segev-i/moria.fridman/anaconda3/bin:$PATH"  ## <<-- Change this to the path that you use
#export PYTHONDIR="/ems/elsc-labs/segev-i/moria.fridman/anaconda3/envs/project/bin/python"

export profile='_'  #Note the profile name, you will need to use it in the python script
ipython profile create --parallel --profile=${profile}


echo "Launching job"
conda init
conda activate project
python main_cell_data.py $1
#conda deactivate
