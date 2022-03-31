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
IDIR='/cluster/work/users/the038/divD_des2021/decor_des2021/regrid_anom/'
IF0=$IDIR'divD.WN0-3.1979-2018.greenland_box.smoothed.anom.90d_rm.regrid.nc'
#IF0i=$IDIR'divD.WN0-3.greenland_box.smoothed.anom.regrid.Icemask.nc'
IF1=$IDIR'divD.WN4-5.1979-2018.greenland_box.smoothed.decorWN0-3.anom.90d_rm.regrid.nc'
#IF1i=$IDIR'divD.WN4-5.1979-2018.greenland_box.smoothed.decorWN0-3.anom.regrid.Icemask.nc'

#IMASK='/cluster/work/users/the038/divD_anom/Icemask_Topo_Iceclasses_lon_lat_average_1km.nc'
#OMASK='/cluster/work/users/the038/divD_anom/Icemask.nc'

# Multiply with icemask, so that only divergences over the ice is considered.
#cdo selvar,Icemask $IMASK $OMASK
#cdo mul $IF0 $OMASK $IF0i
#cdo mul $IF1 $OMASK $IF1i

# Indicies for selindex
# South west region
I1='100'
I2='500'
I3='1'
I4='1400'

# Outfiles
OF0=$IDIR'south_west_divD.WN0-3.1979-2018.anom.90d_rm.nc'
#OF0s=$IDIR'south_west_divD.WN0-3.1979-2018.anom.summed.nc'
OF1=$IDIR'south_west_divD.WN4-5.1979-2018.decorWN0-3.anom.90d_rm.nc'
#OF1s=$IDIR'south_west_divD.WN4-5.1979-2018.decorWN0-3.anom.summed.nc'

cdo selindexbox,$I1,$I2,$I3,$I4 $IF0 $OF0
cdo selindexbox,$I1,$I2,$I3,$I4 $IF1 $OF1
#cdo fldsum $OF0 $OF0s
#cdo fldsum $OF1 $OF1s
## South east region
#I1='550'
#I2='1300'
#I3='1'
#I4='1100'
##
### Outfiles  
##
#OF0=$IDIR'south_east_divD.WN1-3.nc'
#OF0s=$IDIR'south_east_divD.WN1-3.summed.nc'
#OF1=$IDIR'south_east_divD.WN4-5.nc'
#OF1s=$IDIR'south_east_divD.WN4-5.summed.nc'
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
#OF0=$IDIR'north_east_small_divD.WN1-3.nc'
#OF0s=$IDIR'north_east_small_divD.WN1-3.summed.nc'
#OF1=$IDIR'north_east_small_divD.WN4-5.nc'
#OF1s=$IDIR'north_east_small_divD.WN4-5.summed.nc'
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
#OF0s=$IDIR'greenland_divD.WN1-3.summed.nc'
#OF1s=$IDIR'greenland_divD.WN4-5.summed.nc'
#
#cdo fldsum $IF0i $OF0s
#cdo fldsum $IF1i $OF1s


exit 0
