#!/bin/bash -l

##############################
#       Job blueprint        #
##############################

# Give your job a name, so you can recognize it in the queue overview
#SBATCH --job-name=DIV_Q_compute
#SBATCH -A nn9348k
#SBATCH --partition=bigmem
#              d-hh:mm:ss
#SBATCH --time=0-02:00:00
#SBATCH --ntasks=4
#SBATCH --mem-per-cpu=8G

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
/cluster/home/the038/pyvenv/bin/python -u /cluster/home/the038/compute_div_Q/compute_divergence_E.py
#/cluster/home/the038/pyvenv/bin/python -u /cluster/home/the038/compute_div_Q/sum_n.py
#/cluster/home/the038/pyvenv/bin/python -u /cluster/home/the038/compute_div_Q/sel_greenland.py
#/cluster/home/the038/pyvenv/bin/python -u /cluster/home/the038/compute_div_Q/sub_wns.py
#/cluster/home/the038/pyvenv/bin/python -u /cluster/home/the038/compute_div_Q/smooth_div.py
#/cluster/home/the038/pyvenv/bin/python -u /cluster/home/the038/compute_div_Q/anom_div_E.py
#srun -n 12 /cluster/home/the038/pyvenv/bin/python -u /cluster/home/the038/compute_div_Q/smooth_div_mpi.py
#cd /cluster/work/users/the038/divQ_anom/divQ/divergence
#cdo mergetime divQ.WN4-5.????.??.smoothed.greenland_box.nc divQ.WN4-5.1979-2018.greenland_box.smoothed.nc
#cdo mergetime divQ.WN1-3.????.??.smoothed.greenland_box.nc divQ.WN1-3.1979-2018.greenland_box.smoothed.nc


# After everything is saved to the home directory, delete the work directory to
# Finish the script
exit 0
