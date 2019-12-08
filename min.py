#!/usr/bin/env python2

import os
import time
import subprocess
import sys

os.chdir(os.path.dirname(__file__))


def invoke_cmd(cmd):
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return (out, err)


# create containers
cid = [None]*3
def create_containers(data_dirs):
    for i in range(0, len(data_dirs)):
        #server_logs_host.append(os.path.join(uppath(data_dirs[i],1), 'log-' + str(i)))
        dir00 = "%s/etc/glusterfs" % (data_dirs[i])
        dir01 = "%s/var/lib/glusterd" % (data_dirs[i])
        dir02 = "%s/var/log/glusterfs" % (data_dirs[i])
        dir03 = "%s/bricks/brick0" % data_dirs[i]

        # print ("\n\nCreating the .mp dirs")
        # os.system("mkdir -p %s" % dir00);
        # os.system("mkdir -p %s" % dir01);
        # os.system("mkdir -p %s" % dir02);
        # os.system("mkdir -p %s" % dir03);
        
        #raw_input("check or exit?")

        my_cmd1 = """sudo docker run  --name g%s --net netgfs \\
        -v %s:/etc/glusterfs:z \\
        -v %s:/var/lib/glusterd:z \\
        -v %s:/var/log/glusterfs:z \\
        -v %s:/bricks/brick0 \\
        -v /sys/fs/cgroup:/sys/fs/cgroup:ro \\
        -d --privileged=true \\
        gluster/gluster-fedora"""

        docker_run = my_cmd1 % (i+1, dir00, dir01, dir02, dir03)


        print "\n\n", docker_run, "\n\n"
        # raw_input("looping..")

        os.system(docker_run)


# create/start volume
def create_volume(onlystart=False):# probe each other
    time.sleep(5);
    probe1 = 'docker exec -ti g%s bash -c "gluster peer probe g%s.netgfs"' % (1, 2)
    os.system(probe1);
    time.sleep(2);
    os.system('docker exec -ti g1 bash -c "gluster peer status"')
    os.system('docker exec -ti g2 bash -c "gluster peer status"')
    os.system('docker exec -ti g3 bash -c "gluster peer status"')

    probe2 = 'docker exec -ti g%s bash -c "gluster peer probe g%s.netgfs"' % (1, 3)
    os.system(probe2);
    time.sleep(2);
    os.system('docker exec -ti g1 bash -c "gluster peer status"')
    os.system('docker exec -ti g2 bash -c "gluster peer status"')
    os.system('docker exec -ti g3 bash -c "gluster peer status"')

    probe3 = 'docker exec -ti g%s bash -c "gluster peer probe g%s.netgfs"' % (3, 1)
    os.system(probe3);
    time.sleep(2);
    os.system('docker exec -ti g1 bash -c "gluster peer status"')
    os.system('docker exec -ti g2 bash -c "gluster peer status"')
    os.system('docker exec -ti g3 bash -c "gluster peer status"')


    #
    # Volumes
    # 

    os.system('docker exec -ti g1 bash -c "mkdir -p /bricks/brick0/gv0"')
    os.system('docker exec -ti g2 bash -c "mkdir -p /bricks/brick0/gv0"')
    os.system('docker exec -ti g3 bash -c "mkdir -p /bricks/brick0/gv0"')


    create_v = ("gluster volume create gv0 replica 3 g1.netgfs:/bricks/brick0/gv0 g2.netgfs:/bricks/brick0/gv0 g3.netgfs:/bricks/brick0/gv0")
    start_v = ("gluster volume start gv0")
    info_v = ("gluster volume info")
    status_v = "gluster volume status"

    if (not onlystart):
        os.system('docker exec -ti g1 bash -c "%s"' % create_v)

    os.system('docker exec -ti g1 bash -c "%s"' % start_v)
    os.system('docker exec -ti g1 bash -c "%s"' % info_v)

    os.system('docker exec -ti g1 bash -c "%s"' % status_v)


def stop_cont():
    os.system('docker rm $(docker stop -t 0 $(docker ps -aq))')



#
# Execution
# 

# 0. Remove appdir
# os.system("rm -rf ./appdir")

def manual_dir():
    data_dirs = ["./appdir/systems/gl/g1", "./appdir/systems/gl/g2", "./appdir/systems/gl/g3"]
    for i, j in enumerate(data_dirs):
        os.system("mkdir -p %s" % j)
        data_dirs[i] = os.path.abspath(j)
    return data_dirs

# 1. Create cont
create_containers(manual_dir())

# 2. Create vol
create_volume();

# 3. stop and remove containers only (not dirs)
stop_cont();


# 4. recreate the containers
data_dirs = []
for i in range(2, 5):
    data_dirs.append(os.path.abspath(sys.argv[i]))

for i, j in enumerate(data_dirs):
    os.system("mkdir -p %s" % j)
    data_dirs[i] = os.path.abspath(j)

create_containers(data_dirs);


# 5. start the volume
create_volume(True)


# 6. Stop and delete containers again?
raw_input("Stop and delete containers again?");
stop_cont();



