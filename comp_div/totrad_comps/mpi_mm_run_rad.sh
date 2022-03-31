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

#/cluster/home/the038/pyvenv/bin/python -u /cluster/home/the038/regrid_decor_div/regrid_rad.py

#IDIR=/cluster/work/users/the038/radiation/SSH/
#cd $IDIR
#OF=SSH.1979-2019.anom.detrended.10d_rm.regrid.nc
#cdo mergetime SSH.1979-2019.anom.detrended.10d_rm.*.regrid.nc $OF
IDIR=/cluster/work/users/the038/radiation/
cd $IDIR
#IF1=totrad/totrad.1979-2019.anom.10d_rm.regrid.nc
#IF2=reg.totrad.TP.1979-2018.10d_rm.nc
#IF3=TP/TP.1979-2019.anom.10d_rm.regrid.nc
#TF=$SCRATCH'/temp1.nc'
#OF=totrad/totrad.decorTP.1979-2019.anom.10d_rm.regrid.nc
OF=TP/TP.1979-2019.anom.10d_rm.regrid.nc
#cdo mul $IF2 $IF3 $TF
#cdo sub $IF1 $TF $OF



OFN='/cluster/work/users/the038/radiation/TP/TP.1979-2019.anom.10d_rm.regrid.trend.nc'
#OFN='/cluster/work/users/the038/radiation/totrad/totrad.decorTP.1979-2019.anom.10d_rm.regrid.trend.nc'
OF1=$SCRATCH'/divE.temp.nc'
OF2=$SCRATCH'/SMB.temp.nc'
OF3=$SCRATCH'/temp.nc'
OF4=$SCRATCH'/temp2.nc'
OF5=$SCRATCH'/temp3.nc'
OF6=$SCRATCH'/temp4.nc'

cdo select,year=1979/1999 $OF $OF3
cdo select,year=2000/2018 $OF $OF4

cdo timmean $OF3 $OF5
cdo timmean $OF4 $OF6
cdo sub $OF6 $OF5 $OFN




# After everything is saved to the home directory, delete the work directory to
# Finish the script
