#! /bin/bash

CURRENT_DIR=$PWD
CORDS_DIR=$(realpath ../..)

declare d1="a";
declare d2="b";
declare d3="c";

sudo rm -rf ./appdir
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

mkdir -p $CURRENT_DIR/appdir/systems/gl/t

echo -e "\nTracing now..."
cd $CORDS_DIR
./trace.py --trace_files \
    $CURRENT_DIR/appdir/systems/gl/t/trace0 $CURRENT_DIR/appdir/systems/gl/t/trace1 $CURRENT_DIR/appdir/systems/gl/t/trace2 --data_dirs \
    $CURRENT_DIR/appdir/systems/gl/$d1 $CURRENT_DIR/appdir/systems/gl/$d2 $CURRENT_DIR/appdir/systems/gl/$d3 \
    --workload_command $CURRENT_DIR/gluster_read.py --ignore_file $CURRENT_DIR/ignore

echo -e "\nTracing complete..."
