#!/bin/bash -l
#SBATCH --nodes 1
#SBATCH --ntasks 11
#SBATCH --time=00:20:00
#SBATCH --partition=plgrid
#SBATCH --account=plgwtdydoptym-cpu

module load r/4.2.0-foss-2021b
module load python/3.9.6-gcccore-11.2.0

pip install finta
pip install cma

# measure start time
start=$(date +%s)

Rscript irace_script.R

# measure end time
end=$(date +%s)

# calculate runtime
runtime=$((end-start))
echo "Runtime: $runtime seconds"