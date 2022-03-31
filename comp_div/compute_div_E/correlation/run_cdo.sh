#!/bin/bash -l

##############################
#       Job blueprint        #
##############################

# Give your job a name, so you can recognize it in the queue overview
#SBATCH --job-name=compute_correlation
#SBATCH -A nn9348k
#SBATCH --partition=bigmem
#              d-hh:mm:ss
#SBATCH --time=1-0:0:0
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
IF1='/cluster/work/users/the038/Edivdat/divergence/anomalies/regrid/divE.n0.1979-2017.nc'
IF2='/cluster/work/users/the038/Edivdat/divergence/anomalies/regrid/divE.n1-3.1979-2017.rgrid.nc'
IF3='/cluster/work/users/the038/Edivdat/divergence/anomalies/regrid/divE.n4-5.1979-2017.rgrid.nc'
SMB='/cluster/work/users/the038/racmo_smb/smb.anom.1979-2017.nc'
IFN='/cluster/work/users/the038/Edivdat/divergence/anomalies/regrid/divE.n0-5.1979-2017.rgrid.nc'
OFI='/cluster/work/users/the038/Edivdat/correlation/cor.vE.n0-5.SMB.1979-2017.nc'
OFI2='/cluster/work/users/the038/Edivdat/correlation/cor.vE.n0.SMB.1979-2017.nc'
cdo -enssum $IF1 $IF2 $IF3 $IFN
cdo -timcor $SMB $IFN $OFI
# Define and create a unique scratch directory for this job

# You can copy everything you need to the scratch directory
# ${SLURM_SUBMIT_DIR} points to the path where this script was submitted from

# This is where the actual work is done. In this case, the script only waits.
#srun -n 4 /cluster/home/the038/pyvenv/bin/python -u $SCRATCH/div_filemerge/filemerger_fram.py



# After everything is saved to the home directory, delete the work directory to
# Finish the script
exit 0
