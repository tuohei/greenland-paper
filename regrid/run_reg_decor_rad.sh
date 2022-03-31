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

# Prepare input files
SMB='/cluster/work/users/the038/racmo_smb/anomalies/smb.anom.detrended.smoothed10days.nc'
#SMB='/cluster/work/users/the038/racmo_smb/anomalies/smb.anom.detrended.10d_rm.nc'
#IFN='/cluster/work/users/the038/divD-WN0-3/divD.WN0-5.1979-2018.greenland_box.smoothed.decorWN0-3.anom.detrended.10d_rm.nc'
IDIR='/cluster/work/users/the038/divD_des2021/decor_des2021/regrid_runmean/'
#IFN=$IDIR'divD.WN4-5.1979-2018.greenland_box.smoothed.decorWN0-3.anom.detrended.10d_rm.regrid.summed.nc'
IFN=$IDIR'divD.WN0-3.1979-2018.greenland_box.smoothed.anom.detrended.10d_rm.regrid.summed.nc'
#cdo runmean,10 $IFN1 $IFN
OF4=$SCRATCH'/SMB2.temp.nc'
#cdo mergetime divD.WN4-5.1979-2018.greenland_box.smoothed.decorWN0-3.anom.detrended.10d_rm.nc.* $OF4
cdo selvar,divD $IFN $OF4
#cdo chname,divD,divD $IFN 
OF1=$SCRATCH'/divE.temp.nc'
OF2=$SCRATCH'/SMB.temp.nc'
OF3=$SCRATCH'/divE2.temp.nc'
#OF4=$SCRATCH'/divE4.temp.nc'
OF5=$SCRATCH'/divE5.temp.nc'
TFN=$SCRATCH'/temp1.nc'
TSMB=$SCRATCH'/temp2.nc'
# Positive lag
#OFI=$IDIR'reg.divD.WN4-5.decorWN0-3.SMB.1979-2018.10d_rm.summed.nc'
OFI=$IDIR'reg.divD.WN0-3.SMB.1979-2018.10d_rm.summed.nc'
# Negative lag

cdo enlarge,$SMB $OF4 $OF5
cdo timcovar $SMB $OF5 $TFN
cdo timvar $OF5 $OF1

cdo div $TFN $OF1 $OFI




# After everything is saved to the home directory, delete the work directory to
# Finish the script
exit 0
