#!/bin/bash -l

##############################
#       Job blueprint        #
##############################

# Give your job a name, so you can recognize it in the queue overview
#SBATCH --job-name=DIV_regrid
#SBATCH -A nn9348k
#SBATCH --partition=bigmem
#              d-hh:mm:ss
#SBATCH --time=1-0:0:0
#SBATCH --ntasks=8
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

#/cluster/home/the038/pyvenv/bin/python -u /cluster/home/the038/regrid_decor_div/regrid_vQ.py
#/cluster/home/the038/pyvenv/bin/python -u /cluster/home/the038/regrid_decor_div/regrid_vQ2.py
#/cluster/home/the038/pyvenv/bin/python -u /cluster/home/the038/regrid_decor_div/regrid_vD.py
#/cluster/home/the038/pyvenv/bin/python -u /cluster/home/the038/regrid_decor_div/regrid_vD2.py

IDIR=/cluster/work/users/the038/divD_des2021/decor_des2021/
cd $IDIR
IF=divD.WN0-3.1979-2018.greenland_box.smoothed.anom.nc
IF2=divD.WN4-5.1979-2018.greenland_box.smoothed.decorWN0-3.anom.nc
OF=divD.WN0-3.1979-2018.greenland_box.smoothed.anom.90d_rm.nc
OF2=divD.WN4-5.1979-2018.greenland_box.smoothed.decorWN0-3.anom.90d_rm.nc
cdo runmean,180 $IF $OF
cdo runmean,180 $IF2 $OF2

IDIR=/cluster/work/users/the038/divQ_des2021/decor_des2021/
cd $IDIR
IF=divQ.WN0-3.1979-2018.greenland_box.smoothed.anom.nc
IF2=divQ.WN4-5.1979-2018.greenland_box.smoothed.decorWN0-3.anom.nc
OF=divQ.WN0-3.1979-2018.greenland_box.smoothed.anom.90d_rm.nc
OF2=divQ.WN4-5.1979-2018.greenland_box.smoothed.decorWN0-3.anom.90d_rm.nc
cdo runmean,180 $IF $OF
cdo runmean,180 $IF2 $OF2

# After everything is saved to the home directory, delete the work directory to
# Finish the script
exit 0
