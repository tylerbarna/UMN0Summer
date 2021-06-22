#!/bin/bash
#SBATCH --job-name=GW170817
#SBATCH --mail-type=ALL
#SBATCH --mail-user=barna314@umn.edu
#SBATCH --time=11:59:59
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=8gb
#SBATCH -p small
#SBATCH -o %j.out
#SBATCH -e %j.err

module load texlive

source /home/cough052/barna314/anaconda3/bin/activate nmma
export PATH=/home/cough052/barna314/anaconda3/bin/:$PATH
export PATH=/home/cough052/barna314/anaconda3/envs/nmma/bin/:$PATH
which conda

srun run.sh

python3 bestfit_lightcurves_generation.py
python3 plot.py
