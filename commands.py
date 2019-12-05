sudo rm -rf ./appdir
python ./init.py

cd ../CORDS

sudo ./trace.py --trace_files \
    ../gluster/appdir/systems/gl/t/trace0 ../gluster/appdir/systems/gl/t/trace1 ../gluster/appdir/systems/gl/t/trace2 --data_dirs \
    ../gluster/appdir/systems/gl/g1 ../gluster/appdir/systems/gl/g2 ../gluster/appdir/systems/gl/g3 \
    --workload_command ../gluster/gluster_read.py

sudo ./trace.py --trace_files \
    ./trace0 ./trace1 ./trace2 --data_dirs \
    ../gluster/appdir/systems/gl/g1 ../gluster/appdir/systems/gl/g2 ../gluster/appdir/systems/gl/g3 \
    --workload_command ../gluster/gluster_read.py

sudo ./cords.py --trace_files \
    ../gluster/appdir/systems/gl/trace0 ../gluster/appdir/systems/gl/trace1 ../gluster/appdir/systems/gl/trace2 \
    --data_dirs ../gluster/appdir/systems/gl/g1 ../gluster/appdir/systems/gl/g2 ../gluster/appdir/systems/gl/g3 \
    --workload_command ../gluster/gluster_read.py --ignore-file ../gluster/ignore


python ./gluster_read.py cords \
    ./appdir/systems/gl/g1/bricks/brick0 \
    ./appdir/systems/gl/g2/bricks/brick0 \
    ./appdir/systems/gl/g3/bricks/brick0 \
    ../
