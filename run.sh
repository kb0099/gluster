#! /bin/bash

CURRENT_DIR=$PWD
CORDS_DIR=$(realpath ../..)

declare d1="a";
declare d2="b";
declare d3="c";

#sudo rm -rf ./appdir
# Some files don't want to get deleted -> move them

mkdir -p ./trash
mv ./appdir ./trash/appdir
echo -e "\nOld files cleared."

echo -e "\nIniting"
./init.py

mv $CURRENT_DIR/appdir/systems/gl/g1 $CURRENT_DIR/appdir/systems/gl/$d1
mv $CURRENT_DIR/appdir/systems/gl/g2 $CURRENT_DIR/appdir/systems/gl/$d2
mv $CURRENT_DIR/appdir/systems/gl/g3 $CURRENT_DIR/appdir/systems/gl/$d3

docker rm $(docker stop -t 0 $(docker ps -aq))

echo -e "\nTracing now... "
cd ../CORDS
./trace.py --trace_files \
     ./trace0 ./trace1 ./trace2 --data_dirs \
     ../gluster/appdir/systems/gl/$d1 ../gluster/appdir/systems/gl/$d2 ../gluster/appdir/systems/gl/$d3 \
     --workload_command ../gluster/gluster_read.py --ignore_file ../gluster/ignore



# ./cords.py --trace_files \
#     ./trace0 ./trace1 ./trace2 --data_dirs \
#     ../gluster/appdir/systems/gl/$d1 ../gluster/appdir/systems/gl/$d2 ../gluster/appdir/systems/gl/$d3 \
#     --workload_command ../gluster/gluster_read.py

echo -e "\nTracing complete... "
echo -e "\nTrying to unmount again if still mounted. "

cd ../gluster/appdir/systems/gl
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

echo -e "\n Should be done!"
