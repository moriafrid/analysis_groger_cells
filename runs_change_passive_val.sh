#!/bin/bash
#pass 1 argument = size of ipcluster
#pass 2 argument = cell_name
#pass 3 argument = file_type
#pass 4 argument = RA
#pass 5 argument = CM
#pass 6 argument = RM
#pass 7 argument = fit_condition (const_param/different_initial_conditions)
#pass 8 argument = passive_vel_name
#pass 9 argumant = resize_dend_by
#pass 10 argument = shrinkage_by
#pass 11 argument = SPINE_START
#pass 12 argument = folder

# Write output as following (%j is JOB_ID)
#SBATCH -o outputs/output-%j.out
#SBATCH -e errors/error-%j.err
#SBATCH --mem 60000
#SBATCH -t 2-0
#SBATCH -c 1

echo "the number parameters the sbatch get is "$#

args=""
if [[ $# -lt 1 ]] ; then
    echo "Wrong usage. not have enought parameters (must receive script)"
    exit 1
fi

script=$1
shift 1

args=$@
shift $#

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
python MOO_get_parameters.py $args ${profile}
#conda deactivate
