#! /bin/bash

declare d1="g1";
declare d2="g2";
declare d3="g3";

sudo rm -rf ./appdir
# Some files don't want to get deleted -> move them
mkdir -p ./trash
mv ./appdir ./trash/appdir
echo "\nOld files cleared."

echo "\nIniting"
python ./init.py

# mv ../gluster/appdir/systems/gl/g1 ../gluster/appdir/systems/gl/$d1
# mv ../gluster/appdir/systems/gl/g2 ../gluster/appdir/systems/gl/$d2
# mv ../gluster/appdir/systems/gl/g3 ../gluster/appdir/systems/gl/$d3

docker rm $(docker stop -t 0 $(docker ps -aq))

echo "\nTracing now..."
cd ../CORDS
./trace.py --trace_files \
    ../gluster/appdir/systems/gl/t/trace0 ../gluster/appdir/systems/gl/t/trace1 ../gluster/appdir/systems/gl/t/trace2 --data_dirs \
    ../gluster/appdir/systems/gl/$d1/bricks/brick0 ../gluster/appdir/systems/gl/$d2/bricks/brick0 ../gluster/appdir/systems/gl/$d3/bricks/brick0 \
    --workload_command ../gluster/gluster_read.py --ignore_file ../gluster/ignore

echo "\nTracing complete..."
