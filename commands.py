python ./init.py

python ./gluster_read.py cords \
    ./appdir/systems/gl/g1/bricks/brick0 \
    ./appdir/systems/gl/g2/bricks/brick0 \
    ./appdir/systems/gl/g3/bricks/brick0 \
    ../


mkdir -p ../gluster/appdir/systems/gl
sudo ./trace.py --trace_files \
    ../gluster/appdir/systems/gl/trace0 ../gluster/appdir/systems/gl/trace1 ../gluster/appdir/systems/gl/trace2 --data_dirs \
    ../gluster/appdir/systems/gl/g1/bricks/brick0 ../gluster/appdir/systems/gl/g2/bricks/brick0/ ../gluster/appdir/systems/gl/g3/bricks/brick0/ \
    --workload_command ../gluster/gluster_read.py

sudo ./cords.py --trace_files \
    ../gluster/appdir/systems/gl/trace0 ../gluster/appdir/systems/gl/trace1 ../gluster/appdir/systems/gl/trace2 \
    --data_dirs ../gluster/appdir/systems/gl/g1/bricks/brick0 ../gluster/appdir/systems/gl/g2/bricks/brick0/ ../gluster/appdir/systems/gl/g3/bricks/brick0/ \
    --workload_command ../gluster/gluster_read.py
