#!/usr/bin/env python2

import sys
import os
import time
import subprocess
import logging

logging.basicConfig()

uppath = lambda _path, n: os.sep.join(_path.split(os.sep)[:-n])

CURR_DIR = os.path.dirname(os.path.realpath(__file__))

os.system('docker rm $(docker stop -t 0 $(docker ps -aq)) > /dev/null')
time.sleep(5);

data_dirs = []
server_logs = []
server_logs_host = []
log_dir = None

assert len(sys.argv) >= 4
for i in range(2, 5):
	data_dirs.append(sys.argv[i]) 

print "here .... here "
print(data_dirs);
raw_input("exit")
raw_input("exit")
raw_input("exit")

#if logdir specified
if len(sys.argv) == 6:
	log_dir = sys.argv[-1]


def logger_log(log_dir, str):
	if log_dir is not None:
		assert os.path.isdir(log_dir) and os.path.exists(log_dir)
		client_log_file = os.path.join(log_dir, 'log-client')
		with open(client_log_file, 'a') as f:
			f.write(str)
	else:
		print(str.replace('\n', ';'))

def invoke_cmd(cmd):
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()
	return (out, err)

data_dirs = []
log_dir = None

assert len(sys.argv) >= 4
for i in range(2, 5):
	data_dirs.append(sys.argv[i]) 

#if logdir specified
if len(sys.argv) == 6:
	log_dir = sys.argv[-1]


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
    time.sleep(2);

    assert cid[i] is not None
    assert err[i] is None or len(err) == 0

# All nodes have started! Do the workload.
time.sleep(5)
out = ''
err = ''
inited_value = 'a' * 8192

logger_log(log_dir, 'Before workload\n')
to_write = ''


# probe each other
time.sleep(5);
probe1 = 'docker exec -ti g%s bash -c "gluster peer probe g%s.netgfs"' % (1, 2)
os.system(probe1);
time.sleep(2);
probe2 = 'docker exec -ti g%s bash -c "gluster peer probe g%s.netgfs"' % (1, 3)
os.system(probe2);

probe3 = 'docker exec -ti g%s bash -c "gluster peer probe g%s.netgfs"' % (3, 1)
os.system(probe3);


to_write += os.system('docker exec -ti g1 bash -c "gluster peer status"')
to_write += os.system('docker exec -ti g2 bash -c "gluster peer status"')
to_write += os.system('docker exec -ti g3 bash -c "gluster peer status"')


logger_log(log_dir, to_write)
logger_log(log_dir, '----------------------------------------------\n')

server_i = 0
out = ''

for g in ["g1", "g2", "g3"]:
	out_, err_ = invoke_cmd('docker exec -ti %s bash -c "%s"' % (g, "fgrep -o a /bricks/brick0/gv0/test_value | wc -l")  )
	if err_ is None or len(err_) == 0:
		out += 'Successfully read the value at server:' + g + "[" + out_ + "]" ' !\n'
	else:
		err += 'Exception occured:' + str(e) + ' at: ' + g + '\n'		
		time.sleep(5);

logger_log(log_dir, out)
logger_log(log_dir, err)

logger_log(log_dir, '----------------------------------------------\n')

logger_log(log_dir, 'After workload\n')
to_write = ''


out_, err_= invoke_cmd('docker exec -ti g1 bash -c "gluster peer status"')
to_write += out_ + " " + err_
out_, err_ = invoke_cmd('docker exec -ti g2 bash -c "gluster peer status"')
to_write += out_ + " " + err_
out_, err_ = invoke_cmd('docker exec -ti g3 bash -c "gluster peer status"')
to_write += out_ + " " + err_



logger_log(log_dir, to_write)
logger_log(log_dir, '----------------------------------------------\n')


os.system('docker rm $(docker stop -t 0 $(docker ps -aq)) > /dev/null')
