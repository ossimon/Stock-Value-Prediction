#!/bin/bash -l
#SBATCH --nodes 1
#SBATCH --ntasks 31
#SBATCH --time=00:10:00
#SBATCH --partition=plgrid-testing
#SBATCH --account=plgwtdydoptym-cpu

module load r/4.2.0-foss-2021b
module load python/3.9.6-gcccore-11.2.0

source ../venv/bin/activate

# measure start time
start=$(date +%s)

Rscript irace_script.r

# measure end time
end=$(date +%s)

deactivate

# calculate runtime
runtime=$((end-start))
echo "Runtime: $runtime seconds"