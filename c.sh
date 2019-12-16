#! /bin/bash

declare d1="a";
declare d2="b";
declare d3="c";


cd ../CORDS
./cords.py --trace_files \
    ./trace0 ./trace1 ./trace2 --data_dirs \
    ../gluster/appdir/systems/gl/$d1 ../gluster/appdir/systems/gl/$d2 ../gluster/appdir/systems/gl/$d3 \
    --workload_command ../gluster/gluster_read.py

cd -