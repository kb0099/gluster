#!/usr/bin/bash

d1="g1"
d2="g2"
d3="g3"

WORK_DIR=$PWD

cd ./appdir/systems/gl
fusermount -u $d1.mp &> /dev/null
fusermount -u $d3.mp &> /dev/null
fusermount -u $d2.mp &> /dev/null


sudo fusermount -u $d1.mp &> /dev/null
sudo fusermount -u $d3.mp &> /dev/null
sudo fusermount -u $d2.mp &> /dev/null

sudo umount -l $d2.mp &> /dev/null
sudo umount -l $d1.mp &> /dev/null
sudo umount -l $d3.mp &> /dev/null


sudo umount -f $d1.mp &> /dev/null
sudo umount -f $d2.mp &> /dev/null
sudo umount -f $d3.mp &> /dev/null


cd $WORK_DIR/../CORDS
./trace.py --trace_files \
     ./trace0 ./trace1 ./trace2 --data_dirs \
     ../gluster/appdir/systems/gl/g1 ../gluster/appdir/systems/gl/g2 ../gluster/appdir/systems/gl/g3 \
     --workload_command ../gluster/min.py



cd $WORK_DIR/appdir/systems/gl
fusermount -u $d1.mp &> /dev/null
fusermount -u $d3.mp &> /dev/null
fusermount -u $d2.mp &> /dev/null


sudo fusermount -u $d1.mp &> /dev/null
sudo fusermount -u $d3.mp &> /dev/null
sudo fusermount -u $d2.mp &> /dev/null

sudo umount -l $d2.mp &> /dev/null
sudo umount -l $d1.mp &> /dev/null
sudo umount -l $d3.mp &> /dev/null


sudo umount -f $d1.mp &> /dev/null
sudo umount -f $d2.mp &> /dev/null
sudo umount -f $d3.mp &> /dev/null