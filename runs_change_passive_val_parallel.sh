#!/bin/bash
# Write output as following (%j is JOB_ID)
#SBATCH -o logs/%j.out
#SBATCH -e logs/%j.err
#SBATCH --mem 60000
#SBATCH -t 2-0
#SBATCH -n 30

#pass 1 argument = size of ipcluster ##%%
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

echo "the number parameters the sbatch get is "$#

args=""
if [[ $# -lt 1 ]] ; then
    echo "Wrong usage. not have enought parameters (must receive script)"
    exit 1
fi
cell_name=$2
RA=$3
set -x


PWD=$(pwd)
LOGS=$PWD/logs
mkdir -p $LOGS
#
#export PATH="/ems/elsc-labs/segev-i/moria.fridman/anaconda3/bin:$PATH"  ## <<-- Change this to the path that you use
#export PYTHONDIR="/ems/elsc-labs/segev-i/moria.fridman/anaconda3/envs/project/bin/python"

export profile=moria$cell_name$RA  #Note the profile name, you will need to use it in the python script
ipython profile create --parallel --profile=${profile}

# ipcluster stop --profile=${profile} &

ipcluster start --profile=${profile} --n=$1 &
sleep 60

args=$@
shift $#

echo "Launching job"
conda init
conda activate project
echo $PATH
#python MOO_get_parameters.py $1 $2 $3 $4 $5 $6 $7 $8 $9 $10 $11 $12 ${profile}
echo $@ ${profile}
python MOO_get_parameters.py $args ${profile}
