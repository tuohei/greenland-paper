#!/bin/bash -l

##############################
#       Job blueprint        #
##############################

# Give your job a name, so you can recognize it in the queue overview
#SBATCH --job-name=sel_sum_reg_cdo
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
module load CDO/1.9.3-intel-2018a
# Type "module avail MySoftware" to find available modules and versions
# It is also recommended to to list loaded modules, for easier debugging:
module list

#######################################################
## Prepare jobs, moving input files and making sure 
# output is copied back and taken care of
##-----------------------------------------------------

# Prepare input files
IDIR='/cluster/work/users/the038/divQ_des2021/decor_des2021/regrid_runmean/'
IF0=$IDIR'divQ.WN0-3.1979-2018.greenland_box.smoothed.anom.detrended.10d_rm.regrid.nc'
IF0i=$IDIR'divQ.WN0-3.1979-2018.greenland_box.smoothed.anom.detrended.10d_rm.regrid.Icemask.nc'
IF1=$IDIR'divQ.WN4-5.1979-2018.greenland_box.smoothed.decorWN0-3.anom.detrended.10d_rm.regrid.nc'
IF1i=$IDIR'divQ.WN4-5.1979-2018.greenland_box.smoothed.decorWN0-3.anom.detrended.10d_rm.regrid.Icemask.nc'

IMASK='/cluster/work/users/the038/divQ_des2021/decor_des2021/Icemask_Topo_Iceclasses_lon_lat_average_1km.nc'
OMASK='/cluster/work/users/the038/divQ_des2021/decor_des2021/Icemask.nc'

# Multiply with icemask, so that only divergences over the ice is considered.
cdo selvar,Icemask $IMASK $OMASK
cdo mul $IF0 $OMASK $IF0i
cdo mul $IF1 $OMASK $IF1i

# Indicies for selindex
# South west region
I1='100'
I2='500'
I3='1'
I4='1400'

# Outfiles
OF0=$IDIR'divQ.WN0-3.1979-2018.greenland_box.smoothed.anom.detrended.10d_rm.regrid.summed.nc'
#OF0s=$IDIR'south_west_divQ.WN0-3.1979-2018.anom.summed.nc'
OF1=$IDIR'divQ.WN4-5.1979-2018.greenland_box.smoothed.decorWN0-3.anom.detrended.10d_rm.regrid.summed.nc'
#OF1s=$IDIR'south_west_divQ.WN4-5.1979-2018.decorWN0-3.anom.summed.nc'

#cdo selindexbox,$I1,$I2,$I3,$I4 $IF0 $OF0
#cdo selindexbox,$I1,$I2,$I3,$I4 $IF1 $OF1
cdo fldsum $IF0i $OF0
cdo fldsum $IF1i $OF1
## South east region
#I1='550'
#I2='1300'
#I3='1'
#I4='1100'
##
### Outfiles  
##
#OF0=$IDIR'south_east_divQ.WN1-3.nc'
#OF0s=$IDIR'south_east_divQ.WN1-3.summed.nc'
#OF1=$IDIR'south_east_divQ.WN4-5.nc'
#OF1s=$IDIR'south_east_divQ.WN4-5.summed.nc'
#
#cdo selindexbox,$I1,$I2,$I3,$I4 $IF0i $OF0
#cdo selindexbox,$I1,$I2,$I3,$I4 $IF1i $OF1
#cdo fldsum $OF0 $OF0s
#
#cdo fldsum $OF1 $OF1s
#
## North east region
#I1='990'
#I2='1200'
#I3='2300'
#I4='2699'
#
## Outfiles  
#
#OF0=$IDIR'north_east_small_divQ.WN1-3.nc'
#OF0s=$IDIR'north_east_small_divQ.WN1-3.summed.nc'
#OF1=$IDIR'north_east_small_divQ.WN4-5.nc'
#OF1s=$IDIR'north_east_small_divQ.WN4-5.summed.nc'
#
#
### Select region
#cdo selindexbox,$I1,$I2,$I3,$I4 $IF0i $OF0
#cdo selindexbox,$I1,$I2,$I3,$I4 $IF1i $OF1
### Sum over region
#cdo fldsum $OF0 $OF0s
#cdo fldsum $OF1 $OF1s
#
##SUM all Greenland
#OF0s=$IDIR'greenland_divQ.WN1-3.summed.nc'
#OF1s=$IDIR'greenland_divQ.WN4-5.summed.nc'
#
#cdo fldsum $IF0i $OF0s
#cdo fldsum $IF1i $OF1s


exit 0
