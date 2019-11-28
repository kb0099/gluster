#!/usr/bin/env  python

import sys
import os
import time
import subprocess
import logging

#
# helpers
# 

def invoke_cmd(cmd):
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()
	return (out, err)


logging.basicConfig()

CURR_DIR = os.path.dirname(os.path.realpath(__file__))

os.system('docker rm $(docker stop -t 0 $(docker ps -aq))')
os.system('docker container prune -f')

# input("exit now");

#input("Exit NOw...")
# os.system('rm -rf trace*')

# os.system('rm -rf workload_dir0*')
# os.system('mkdir workload_dir0')

# os.system('rm -rf workload_dir1*')
# os.system('mkdir workload_dir1')

# os.system('rm -rf workload_dir2*')
# os.system('mkdir workload_dir2')

# os.system ('docker network rm netgfs')
# server_dirs = ['/appdir/systems/rethinkdb/workload_dir0', '/appdir/systems/rethinkdb/workload_dir1', '/appdir/systems/rethinkdb/workload_dir2']

glroot = CURR_DIR + "/appdir/systems/gl"
wl_dirs = [glroot + "/g1/data/gv0", glroot + "/g2/data/gv0", glroot + "/g3/data/gv0"] # work_load direcctories

print CURR_DIR

print glroot
print wl_dirs

dir00 = "%s/g1/etc/glusterfs" % glroot
dir01 = "%s/g1/var/lib/glusterd" % glroot
dir02 = "%s/g1/var/log/glusterfs" % glroot
dir03 = "%s/g1/data/gv0" %glroot # working dir equivalent

invoke_cmd("mkdir -p %s" % dir00)
invoke_cmd("mkdir -p %s" % dir01)
invoke_cmd("mkdir -p %s" % dir02)
invoke_cmd("mkdir -p %s" % dir03)

my_cmd0 = "docker network create netgfs"
my_cmd1 = """docker run  --name g1 --net netgfs \\
-v %s:/etc/glusterfs:z \\
-v %s:/var/lib/glusterd:z \\
-v %s:/var/log/glusterfs:z \\
-v %s:/mnt/gv0 \\
-d --privileged=true \\
gluster/gluster-fedora"""

my_cmd1 = my_cmd1 % (dir00, dir01, dir02, dir03)
#print my_cmd0
#os.system(my_cmd0)

print my_cmd1
invoke_cmd(my_cmd1)


# 
# instance 2
# 


dir00 = "%s/g2/etc/glusterfs" % glroot
dir01 = "%s/g2/var/lib/glusterd" % glroot
dir02 = "%s/g2/var/log/glusterfs" % glroot
dir03 = "%s/g2/data/gv0" %glroot # working dir equivalent

os.system("mkdir -p %s" % dir00)
os.system("mkdir -p %s" % dir01)
os.system("mkdir -p %s" % dir02)
os.system("mkdir -p %s" % dir03)

#my_cmd0 = "docker network create netgfs"
my_cmd1 = """docker run  --name g2 --net netgfs \\
-v %s:/etc/glusterfs:z \\
-v %s:/var/lib/glusterd:z \\
-v %s:/var/log/glusterfs:z \\
-v %s:/mnt/gv0 \\
-d --privileged=true \\
gluster/gluster-fedora"""

my_cmd1 = my_cmd1 % (dir00, dir01, dir02, dir03)
#print my_cmd0
#invoke_cmd(my_cmd0)

print my_cmd1
invoke_cmd(my_cmd1)


#
# instance 3
# 


dir00 = "%s/g3/etc/glusterfs" % glroot
dir01 = "%s/g3/var/lib/glusterd" % glroot
dir02 = "%s/g3/var/log/glusterfs" % glroot
dir03 = "%s/g3/data/gv0" %glroot # working dir equivalent

os.system("mkdir -p %s" % dir00)
os.system("mkdir -p %s" % dir01)
os.system("mkdir -p %s" % dir02)
os.system("mkdir -p %s" % dir03)

#my_cmd0 = "docker network create netgfs"
my_cmd1 = """docker run  --name g3 --net netgfs \\
-v %s:/etc/glusterfs:z \\
-v %s:/var/lib/glusterd:z \\
-v %s:/var/log/glusterfs:z \\
-v %s:/mnt/gv0 \\
-d --privileged=true \\
gluster/gluster-fedora"""

my_cmd1 = my_cmd1 % (dir00, dir01, dir02, dir03)
#print my_cmd0
#invoke_cmd(my_cmd0)

print my_cmd1
out, err = invoke_cmd(my_cmd1)

print "\n\nout = ", out, "\nerr = ", err;

assert out is not None
assert err is None or len(err) == 0



input("Exit NOw...")

# All nodes have started! Do the init.
time.sleep(5)
value = 'a' * 8192
out = ''
err = ''

# probe each other
probe1 = 'docker exec -ti g%s bash -c "gluster peer probe g%s.netgfs"' % (1, 2)
probe1 = 'docker exec -ti g%s bash -c "gluster peer probe g%s.netgfs"' % (1, 3)
probe1 = 'docker exec -ti g%s bash -c "gluster peer probe g%s.netgfs"' % (3, 1)


print out, err
#invoke_cmd('docker rm $(docker stop -t 0 $(docker ps -aq))')
