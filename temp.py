#!/usr/bin/env python2

import sys
import os
import time
import subprocess
import logging

uppath = lambda _path, n: os.sep.join(_path.split(os.sep)[:-n])

dr =  "./appdir/systems/gl/g1/bricks/brick0"
print "0 = ", uppath(dr, 0);
print uppath(dr, 1);
print uppath(dr, 2);
print uppath(dr, 3);
print uppath(dr, 4);
print uppath(dr, 5);


CORDS_HOME = "/home/me/ws/CORDS";
print os.path.abspath(CORDS_HOME);

data_dir_i = "./appdir/systems/gl/g1/bricks/brick0"
print os.path.abspath(data_dir_i);

data_dir_i = os.path.abspath(data_dir_i)
glroot = uppath(data_dir_i, 3);
print "glroot = ", glroot

wl_dirs = [glroot + "/g1/bricks/brick0", glroot + "/g2/bricks/brick0", glroot + "/g3/bricks/brick0"] # work_load direcctories


docker_run = ["", "", ""]
cid = [None]*3
err = [None]*3

data_dirs = [
    "/home/me/ws/gluster/appdir/systems/gl/g1/bricks/brick0",
    "/home/me/ws/gluster/appdir/systems/gl/g2/bricks/brick0",
    "/home/me/ws/gluster/appdir/systems/gl/g3/bricks/brick0"
    ]


glroot = uppath(data_dirs[0], 3);
for i in range(0, len(data_dirs)):
    dir00 = "%s/g%s/etc/glusterfs" % (glroot,i+1)
    dir01 = "%s/g%s/var/lib/glusterd" % (glroot,i+1)
    dir02 = "%s/g%s/var/log/glusterfs" % (glroot,i+1)
    dir03 = data_dirs[i]
    my_cmd1 = """docker run  --name g%s --net netgfs \\
    -v %s:/etc/glusterfs:z \\
    -v %s:/var/lib/glusterd:z \\
    -v %s:/var/log/glusterfs:z \\
    -v %s:/bricks/brick0 \\
    -v /sys/fs/cgroup:/sys/fs/cgroup:ro \\
    -d --privileged=true \\
    gluster/gluster-fedora""";

    docker_run[i] = my_cmd1 % (i+1, dir00, dir01, dir02, dir03)

    print "\n\n", docker_run[i]
    raw_input();

    cid[i],err[i] =  invoke_cmd(docker_run[i])
    assert cid[i] is not None
    assert err[i] is None or len(err) == 0

