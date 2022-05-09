#!/bin/bash
# run with: sbatch <script name> <cell name>

# Write output as following (%j is JOB_ID)
#SBATCH -o logs/%j.out
#SBATCH -e logs/%j.err
# Ask for one CPU, one GPU, enter the GPU queue, and limit run to 1 days
#SBATCH -p ss.q
#SBATCH --mem 10000
#SBATCH -c 1
#SBATCH -t 1-0
#SBATCH --exclude=ielsc-48,ielsc-49
# check if script is started via SLURM or bash
# if with SLURM: there variable '$SLURM_JOB_ID' will exist

echo "the number parameters the function get is "$#

if [[ $# -ne 3 ]] ; then
    echo "Wrong usage. not have enought parameters"
    exit 1
fi

cell_name=$1
shift $#

# `if [ -n $SLURM_JOB_ID ]` checks if $SLURM_JOB_ID is not an empty string
if [ -n $SLURM_JOB_ID ]; then
# check the original location through scontrol and $SLURM_JOB_ID
   SCRIPT_PATH=$(scontrol show job $SLURM_JOBID | awk -F= '/Command=/{print $2}' | cut -d" " -f1)
else
# otherwise: started with bash. Get the real location.
   SCRIPT_PATH=$(realpath $0)
fi
# get script's path to allow running from any folder without errors
path=$(dirname $SCRIPT_PATH)

# put your script here - example script is sitting with this bash script
echo python3 $path/main_cell_data.py $cell_name
python3 $path/main_cell_data.py $cell_name

echo python3 $path/file_converter_to_swc.py $cell_name
python3 $path/file_converter_to_swc.py $cell_name

echo python3 $path/file_converter_to_swc_z_corrections.py $cell_name
python3 $path/file_converter_to_swc_z_corrections.py $cell_name

#echo python3 $path/clear_syn.py $cell_name
#echo "before run the execute_level1 remaind to choose the correct syn from the diraction" $folder $save_dir
#python3 $path/clear_syn.py $cell_name $folder $save_dir $save_dir
#echo "execute_main is complite to run"

