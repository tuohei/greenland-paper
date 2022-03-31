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
#SBATCH --ntasks=6
#SBATCH --mem-per-cpu=8G

# Loading Software modules
# Allways be explicit on loading modules and setting run time environment!!!
module --quiet purge            # Restore loaded modules to the default
module load foss/2018a
module load Python/3.7.4-GCCcore-8.3.0
module load CDO/1.9.8-intel-2019b
# Type "module avail MySoftware" to find available modules and versions
# It is also recommended to to list loaded modules, for easier debugging:
module list

#######################################################
## Prepare jobs, moving input files and making sure 
# output is copied back and taken care of
##-----------------------------------------------------
IF1='/cluster/work/users/the038/divQ-WN4-5/regrid_WN4-5/divQ.WN4-5.1979-2018.greenland_box.smoothed.decorWN0-3.anom.south_west.nc'
#IF2='/cluster/work/users/the038/divQ-WN0-3/regrid_WN0-3/divQ.WN0-3.1979-2018.greenland_box.smoothed.addedWN4-5.anom.south_west.nc'
#IF2='/cluster/work/users/the038/divQ-WN0-3/regrid_WN0-3/divQ.WN0-5.1979-2018.greenland_box.smoothed.anom.south_west.nc'
reg1='/cluster/work/users/the038/divQ-WN4-5/reg.divQ.WN4-5.SMB.1979-2018.60d_rm.south_west.nc'
#reg2='/cluster/work/users/the038/divQ-WN0-3/reg.divQ.WN0-3.SMB.1979-2018.60d_rm.south_west.nc'
#reg2='/cluster/work/users/the038/divQ-WN0-3/reg.divQ.WN0-5.SMB.1979-2018.60d_rm.south_west.nc'

OF1='/cluster/work/users/the038/divQ-WN4-5/regrid_WN4-5/divQ.WN4-5.1979-2018.60d_rm.smoothed.decorWN0-3.anom.south_west.to_smb.nc'
#OF2='/cluster/work/users/the038/divQ-WN0-3/regrid_WN0-3/divQ.WN0-3.1979-2018.60d_rm.smoothed.addedWN4-5.anom.south_west.to_smb.nc'
#OF2='/cluster/work/users/the038/divQ-WN0-3/regrid_WN0-3/divQ.WN0-5.1979-2018.60d_rm.smoothed.anom.south_west.to_smb.nc'
#OF3='/cluster/work/users/the038/divQ-WN4-5/reg.divQ.WN4-5.SMB.1979-2018.10d_rm.south_west.nc'
#OF4='/cluster/work/users/the038/divQ-WN0-3/reg.divQ.WN0-3.SMB.1979-2018.10d_rm.south_west.nc'

#cdo selindexbox,100,500,1,1400 $IF1 $OF1
#cdo selindexbox,100,500,1,1400 $IF2 $OF2
#cdo selindexbox,100,500,1,1400 $IF3 $OF3
#cdo selindexbox,100,500,1,1400 $IF4 $OF4

cdo mul $reg1 $IF1 $OF1
#cdo mul $reg2 $IF2 $OF2


# After everything is saved to the home directory, delete the work directory to
# Finish the script
exit 0
