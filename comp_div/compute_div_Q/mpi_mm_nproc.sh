#!/bin/bash -l

##############################
#       Job blueprint        #
##############################

# Give your job a name, so you can recognize it in the queue overview
#SBATCH --job-name=DIV_Q_compute
#SBATCH -A nn9348k
#SBATCH --partition=normal
#              d-hh:mm:ss
#SBATCH --time=0-02:00:00
#SBATCH --nodes=11

# Loading Software modules
# Allways be explicit on loading modules and setting run time environment!!!
module --quiet purge            # Restore loaded modules to the default
module load foss/2018a
module load Python/3.7.4-GCCcore-8.3.0
module load CDO/1.9.3-intel-2018a

# It is also recommended to to list loaded modules, for easier debugging:
module list

#######################################################
## Prepare jobs, moving input files and making sure 
# output is copied back and taken care of
##-----------------------------------------------------

# Prepare input files
#cp -r /cluster/home/the038/compute_div_E/ $SCRATCH
#cd $SCRATCH/div_filemerge/



# Define and create a unique scratch directory for this job

# You can copy everything you need to the scratch directory
# ${SLURM_SUBMIT_DIR} points to the path where this script was submitted from

# This is where the actual work is done. In this case, the script only waits.
#srun -n 5 /cluster/home/the038/pyvenv/bin/python -u $SCRATCH/div_filemerge/filemerger_fram.py
#/cluster/home/the038/pyvenv/bin/python -u /cluster/home/the038/compute_div_Q/compute_divergence_E.py
/cluster/home/the038/pyvenv/bin/python -u /cluster/home/the038/compute_div_Q/sum_n.py
#/cluster/home/the038/pyvenv/bin/python -u /cluster/home/the038/compute_div_Q/smooth_div.py
#srun -n 324 /cluster/home/the038/pyvenv/bin/python -u /cluster/home/the038/compute_div_Q/smooth_div_mpi.py



# After everything is saved to the home directory, delete the work directory to
# Finish the script
exit 0
