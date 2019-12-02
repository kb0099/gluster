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


# raw_input("exit now");


logging.basicConfig()

CURR_DIR = os.path.dirname(os.path.realpath(__file__))

os.system('docker rm $(docker stop -t 0 $(docker ps -aq))')
os.system('docker network create netgfs')
time.sleep(5);
os.system('docker container prune -f')
os.system('docker container prune -f')
os.system('docker container prune -f')
os.system('docker container prune -f')
os.system('docker container prune -f')
os.system('docker container prune -f')
time.sleep(2);
os.system('docker ps -a')

glroot = CURR_DIR + "/appdir/systems/gl"
wl_dirs = [glroot + "/g1/bricks/brick0", glroot + "/g2/bricks/brick0", glroot + "/g3/bricks/brick0"] # work_load direcctories

print CURR_DIR
print "removing glroot: ", glroot;
os.system("rm -rf %s"%glroot)

dir00 = "%s/g1/etc/glusterfs" % glroot
dir01 = "%s/g1/var/lib/glusterd" % glroot
dir02 = "%s/g1/var/log/glusterfs" % glroot
dir03 = "%s/g1/bricks/brick0" %glroot # working dir equivalent

invoke_cmd("mkdir -p %s" % dir00)
invoke_cmd("mkdir -p %s" % dir01)
invoke_cmd("mkdir -p %s" % dir02)
invoke_cmd("mkdir -p %s" % dir03)

my_cmd0 = "docker network create netgfs"
time.sleep(1);
my_cmd1 = """docker run  --name g1 --net netgfs \\
-v %s:/etc/glusterfs:z \\
-v %s:/var/lib/glusterd:z \\
-v %s:/var/log/glusterfs:z \\
-v %s:/bricks/brick0 \\
-v /sys/fs/cgroup:/sys/fs/cgroup:ro \\
-d --privileged=true \\
gluster/gluster-fedora"""

my_cmd1 = my_cmd1 % (dir00, dir01, dir02, dir03)
#print my_cmd0
#os.system(my_cmd0)


print "\n\n\n"
print my_cmd1
cid,err = invoke_cmd(my_cmd1)
print "\n\n cid = [", cid, "]"
#raw_input("exit now: &c");
# 
# instance 2
# 


dir00 = "%s/g2/etc/glusterfs" % glroot
dir01 = "%s/g2/var/lib/glusterd" % glroot
dir02 = "%s/g2/var/log/glusterfs" % glroot
dir03 = "%s/g2/bricks/brick0" %glroot # working dir equivalent

os.system("mkdir -p %s" % dir00)
os.system("mkdir -p %s" % dir01)
os.system("mkdir -p %s" % dir02)
os.system("mkdir -p %s" % dir03)

#my_cmd0 = "docker network create netgfs"
time.sleep(1);
my_cmd1 = """docker run  --name g2 --net netgfs \\
-v %s:/etc/glusterfs:z \\
-v %s:/var/lib/glusterd:z \\
-v %s:/var/log/glusterfs:z \\
-v %s:/bricks/brick0 \\
-v /sys/fs/cgroup:/sys/fs/cgroup:ro \\
-d --privileged=true \\
gluster/gluster-fedora"""

my_cmd1 = my_cmd1 % (dir00, dir01, dir02, dir03)
#print my_cmd0
#invoke_cmd(my_cmd0)


print "\n\n\n"
print my_cmd1
invoke_cmd(my_cmd1)


#
# instance 3
# 


dir00 = "%s/g3/etc/glusterfs" % glroot
dir01 = "%s/g3/var/lib/glusterd" % glroot
dir02 = "%s/g3/var/log/glusterfs" % glroot
dir03 = "%s/g3/bricks/brick0" %glroot # working dir equivalent

os.system("mkdir -p %s" % dir00)
os.system("mkdir -p %s" % dir01)
os.system("mkdir -p %s" % dir02)
os.system("mkdir -p %s" % dir03)

#my_cmd0 = "docker network create netgfs"
time.sleep(1)
my_cmd1 = """docker run  --name g3 --net netgfs \\
-v %s:/etc/glusterfs:z \\
-v %s:/var/lib/glusterd:z \\
-v %s:/var/log/glusterfs:z \\
-v %s:/bricks/brick0 \\
-v /sys/fs/cgroup:/sys/fs/cgroup:ro \\
-d --privileged=true \\
gluster/gluster-fedora"""

my_cmd1 = my_cmd1 % (dir00, dir01, dir02, dir03)
#print my_cmd0
#invoke_cmd(my_cmd0)


print "\n\n\n"
print my_cmd1
out, err = invoke_cmd(my_cmd1)

print "\n\nout = ", out, "\nerr = ", err;

assert out is not None
assert err is None or len(err) == 0



#x = raw_input("Exit Now? :^c")

# All nodes have started! Do the init.
#time.sleep(5)

test_value = 'a' * 8192;

# probe each other
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

os.system('docker exec -ti g1 bash -c "%s"' % create_v)
os.system('docker exec -ti g1 bash -c "%s"' % start_v)
os.system('docker exec -ti g1 bash -c "%s"' % info_v)


#
# test
# 

mount_v = "mount -t glusterfs g1:/gv0 /mnt"
prep_test = "mkdir -p /var/log; cd /var/log; touch test_value; echo '%s' > test_value" %  test_value
do_test = "cp -rp /var/log/test_value /mnt/test_value"

print("where is the issue 0");
os.system('docker exec -ti g1 bash -c "%s"' % mount_v)
print("where is the issue 1");
os.system('docker exec -ti g1 bash -c "%s"' % prep_test)
print("where is the issue 2");
os.system('docker exec -ti g1 bash -c "%s"' % do_test)


os.system('docker exec -ti g1 bash -c "%s"' % "fgrep -o a /mnt/test_value | wc -l")
os.system('docker exec -ti g2 bash -c "%s"' % "fgrep -o a /bricks/brick0/gv0/test_value | wc -l")
os.system('docker exec -ti g3 bash -c "%s"' % "fgrep -o a /bricks/brick0/gv0/test_value | wc -l")

raw_input("Stop and Prune? Any key : ^C")
os.system('docker rm $(docker stop -t 0 $(docker ps -aq))')
time.sleep(5);
my_cmd0 = "docker network rm netgfs"

