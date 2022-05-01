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
# check if script is started via SLURM or bash
# if with SLURM: there variable '$SLURM_JOB_ID' will exist
#SBATCH --exclude=ielsc-48,ielsc-49

echo $#
echo $@


if [[ $# -ne 8 ]] ; then
    echo "Wrong usage. not have enought parameters"
    exit 1
fi

cell_name=$1
file_type2read=$2
fit_condition=$3
name=$4
resize_diam=$5
shrinkage_factor=$6
SPINE_START=$7
double_spine=$8

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

#echo python3 $path/analysis_fit_after_run.py $cell_name $file_type2read
#python3 $path/analysis_fit_after_run.py $cell_name $file_type2read $resize_diam $shrinkage_factor $SPINE_START $folder

echo python3 $path/Rin_Rm_plot.py $cell_name $file_type2read
python3 $path/Rin_Rm_plot.py $cell_name $file_type2read $fit_condition $name $resize_diam $shrinkage_factor $SPINE_START $double_spine

echo python3 $path/attenuations.py $cell_name $file_type2read $passive_val "True"
python3 $path/attenuations.py  $cell_name $file_type2read $fit_condition $name "False" $resize_diam $shrinkage_factor $SPINE_START $double_spine

echo python3 $path/attenuations.py $cell_name $file_type2read $passive_val "False"
python3 $path/attenuations.py  $cell_name $file_type2read $fit_condition $name "True" $resize_diam $shrinkage_factor $SPINE_START $double_spine

echo python3 $path/dendogram.py $cell_name $file_type2read
python3 $path/dendogram.py $cell_name $file_type2read $fit_condition $name $resize_diam $shrinkage_factor $SPINE_START $double_spine
