# .bash_profile

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
	. ~/.bashrc
fi

# User specific environment and startup programs

#C, Fortran Compiler
 export FC=ifort
 export F90=ifort
 export CC=gcc

 export TOOLS=/opt/local

# # GRADS
# export GRADS=$TOOLS/grads
# export GASCRP=$GRADS/gslib
# export GADDIR=$GRADS/data
# PATH=$PATH:$GRADS/bin

# # HDF5
# export HDF5=$TOOLS/hdf5
# export HDF5_HOME=$HDF5
# export HDF5_LIB=$HDF5_HOME/lib
# export HDF5_INC=$HDF5_HOME/include
# PATH=$PATH:$HDF5_HOME/bin
# LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HDF5_LIB

# # NetCDF
 export NETCDF=$TOOLS/netcdf
 export NETCDFHOME=$NETCDF
 export NETCDF_LIB=$NETCDF/lib
 export NETCDF_INC=$NETCDF/include
 PATH=$PATH:$NETCDFHOME/bin
 LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$NETCDF_LIB

# # grib2,libpng,zlib,jasper
# export JASPER=$TOOLS/jasper
# export JASPERLIB="$TOOLS/jasper/lib -L$TOOLS/zlib/lib -L$TOOLS/libpng/lib"
# export JASPERINC="$TOOLS/jasper/include -I$TOOLS/zlib/include -I$TOOLS/libpng/include"
# LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$TOOLS/libpng/lib:$TOOLS/zlib/lib:$TOOLS/jasper/lib$TOOLS/jasper/lib/jasper
# PATH=$PATH:$TOOLS/wgrib2

# WRF
 export WRF_EM_CORE=1
 export WRF_NCD_LARGE_FILE_SUPPORT=1
 export WRFIO_NCD_LARGE_FILE_SUPPORT=1
 export MP_STACK_SIZE=6400000000

# # NCL
# export NCARG_ROOT=$TOOLS/ncl
# PATH=$PATH:$NCARG_ROOT/bin

# # epstool,pdfcrop
# PATH=$PATH:$TOOLS/epstool/bin:$TOOLS/pdfcrop

# ulimit -s unlimited

# export PATH
# export LD_LIBRARY_PATH

 PATH=$PATH:$HOME/.local/bin:$HOME/bin
#
 export PATH
