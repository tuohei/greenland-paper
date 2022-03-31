#!/bin/bash -l

##############################
#       Job blueprint        #
##############################

# Give your job a name, so you can recognize it in the queue overview
#SBATCH --job-name=merge_div
#SBATCH -A nn9348k
#SBATCH --partition=bigmem
#              d-hh:mm:ss
#SBATCH --time=2-0:0:0
#SBATCH --ntasks=4
#SBATCH --mem-per-cpu=8G

# Loading Software modules
# Allways be explicit on loading modules and setting run time environment!!!
module --quiet purge            # Restore loaded modules to the default
module load foss/2018a
module load Python/3.7.4-GCCcore-8.3.0
module load CDO/1.9.3-intel-2018a
# Type "module avail MySoftware" to find available modules and versions
# It is also recommended to to list loaded modules, for easier debugging:
module list

#######################################################
## Prepare jobs, moving input files and making sure 
# output is copied back and taken care of
##-----------------------------------------------------

# Prepare input files
OFI='/cluster/work/users/the038/correlation/cor.n1-3.SMB.1979-2017.nc'
#cdo -enssum $IF1 $IF2 $IF3 $OFI
cd /cluster/work/users/the038/Edivdat/divergence/anomalies/regrid/
#cdo -timcor $SMB $IFN $OFI
cdo mergetime divQ.n0.*.nc divE.n0.1979-2017.nc
cdo mergetime divQ.n1.*.nc divE.n1.1979-2017.nc
cdo mergetime divQ.n2.*.nc divE.n2.1979-2017.nc
cdo mergetime divQ.n3.*.nc divE.n3.1979-2017.nc
cdo mergetime divQ.n4.*.nc divE.n4.1979-2017.nc
cdo mergetime divQ.n5.*.nc divE.n5.1979-2017.nc
# Define and create a unique scratch directory for this job

# You can copy everything you need to the scratch directory
# ${SLURM_SUBMIT_DIR} points to the path where this script was submitted from

# This is where the actual work is done. In this case, the script only waits.
#srun -n 4 /cluster/home/the038/pyvenv/bin/python -u $SCRATCH/div_filemerge/filemerger_fram.py



# After everything is saved to the home directory, delete the work directory to
# Finish the script
exit 0
