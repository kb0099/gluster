#!/usr/bin/env python2

import sys
import os
import time
import subprocess
import logging

logging.basicConfig()


def uppath(_path, n): return os.sep.join(_path.split(os.sep)[:-n])


CURR_DIR = os.path.dirname(os.path.realpath(__file__))

os.system('docker rm $(docker stop -t 0 $(docker ps -aq)) > /dev/null')
#time.sleep(5)

data_dirs = []
server_logs = []
server_logs_host = []
log_dir = None

assert len(sys.argv) >= 4
for i in range(2, 5):
    data_dirs.append(os.path.abspath(sys.argv[i]))

print ("Actual data dirs:")
print(data_dirs)
# raw_input("exit")
# raw_input("exit")
# raw_input("exit")

# if logdir specified
if len(sys.argv) == 6:
    log_dir = sys.argv[-1]

print "\n\n-------------------------------------\n\nlog dir = [%s]\n\n" % log_dir

def logger_log(log_dir, str):
    # print "\n\n------------------------------------------------- in logger -------------------------------------------\n\n"
    # print "param, str = [%s]" % str
    if log_dir is not None:
        assert os.path.isdir(log_dir) and os.path.exists(log_dir)
        client_log_file = os.path.join(log_dir, 'log-client')
        with open(client_log_file, 'a') as f:
            f.write(str)
    else:
        print(str.replace('\n', ';'))


def invoke_cmd(cmd):
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return (out, err)

glroot = uppath(data_dirs[0], 1)
print "glroot = ", glroot

#raw_input("exit?");

cid = [None]*3
out = ''
err = ''
for i in range(0, len(data_dirs)):
    server_logs_host.append(os.path.join(uppath(data_dirs[i],1), 'log-' + str(i)))
    dir00 = "%s/etc/glusterfs" % (data_dirs[i])
    dir01 = "%s/var/lib/glusterd" % (data_dirs[i])
    dir02 = "%s/var/log/glusterfs" % (data_dirs[i])
    dir03 = "%s/bricks/brick0" % data_dirs[i]

    print ("\n\nCreating the .mp dirs")
    os.system("mkdir -p %s" % dir00);
    os.system("mkdir -p %s" % dir01);
    os.system("mkdir -p %s" % dir02);
    os.system("mkdir -p %s" % dir03);
    
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

    cid[i], err_ = invoke_cmd(docker_run)
    print "cid, err", cid[i], err_
    err += err_
    #time.sleep(2)


    assert cid[i] is not None
    assert err is None or len(err) == 0

# All nodes have started! Do the workload.
#time.sleep(5)
inited_value = 'a' * 8192

logger_log(log_dir, 'Before workload\n')
out = ''


# probe each other
#time.sleep(5)
probe1 = 'docker exec -ti g%s bash -c "gluster peer probe g%s.netgfs"' % (1, 2)
os.system(probe1)
#time.sleep(2)
probe2 = 'docker exec -ti g%s bash -c "gluster peer probe g%s.netgfs"' % (1, 3)
os.system(probe2)

probe3 = 'docker exec -ti g%s bash -c "gluster peer probe g%s.netgfs"' % (3, 1)
os.system(probe3)


#os.system('docker exec -ti g1 bash -c "gluster peer status"')
# out += "g1:: " + out_ + " " + err_
#os.system('docker exec -ti g2 bash -c "gluster peer status"')
# out += "g2:: " + out_ + " " + err_
#os.system('docker exec -ti g3 bash -c "gluster peer status"')
# out += "g3:: " + out_ + " " + err_

# 
#  before workload part
# 
is_running = {"g1": False, "g2": False, "g3" : False}
for g in ["g1", "g2", "g3"]:
    proc_command = 'docker exec -ti %s bash -c  "ps aux | grep glust"' % g

    #print "proc_command = ", proc_command

    out2, err2 = invoke_cmd(proc_command)

    processes = out2.split("\n")
    processes = [p for p in processes if len(p) > 0]
    is_running[g] = False

    # print "processes = ", processes
    if len(processes) >= 2:
        for process_line in processes:
            if "/usr/sbin/glusterd" in process_line:
                #print "line = ", process_line
                is_running[g] = True

print "is_running = ", is_running
for g in [x for x in ["g1", "g2", "g3"] if is_running[x]]:
    out += "Server %s is running.\n" % g
    print "in loop: out = ", out

logger_log(log_dir, out)
logger_log(log_dir, '----------------------------------------------\n')

server_i = 0
out = ''


#
# workload part
# 
failure_str = "Connection failed. Please check if gluster daemon is operational."


for g in [x for x in ["g1", "g2", "g3"] if is_running[x]]:
    out_, err_ = invoke_cmd('docker exec -ti %s bash -c "%s"' %
                            (g, "fgrep -o a /bricks/brick0/gv0/test_value | wc -l"))
    if err_ is None or len(err_) == 0:
        print "\n\n--------------------------------------"
        out_ =  out_.strip().replace('\n', '')
        print "stripped out = ", out_, "type = ", type(out_)
        if out_ == "8192":
            out += '\n%s:: Successfully read the value.\n' % g
        else:
            if failure_str in out_:
                out += "\n%s:: Server not running. Not connecting.\n"
            else:
                out += '\n%s:: Problem at the server : wrong value.\n' % g
    else:
        err += ("\ng%s:: Exception occured:" % g) + str(err_) + "\n"
        
        time.sleep(2)

logger_log(log_dir, out)
logger_log(log_dir, err)

logger_log(log_dir, '----------------------------------------------\n')

logger_log(log_dir, 'After workload\n')
out = ''

# after part

is_running = {"g1": False, "g2": False, "g3" : False}
for g in ["g1", "g2", "g3"]:
    proc_command = 'docker exec -ti %s bash -c  "ps aux | grep glust"' % g

    #print "proc_command = ", proc_command

    out2, err2 = invoke_cmd(proc_command)

    processes = out2.split("\n")
    processes = [p for p in processes if len(p) > 0]
    is_running[g] = False

    # print "processes = ", processes
    if len(processes) >= 2:
        for process_line in processes:
            if "/usr/sbin/glusterd" in process_line:
                #print "line = ", process_line
                is_running[g] = True

print "is_running = ", is_running
for g in [x for x in ["g1", "g2", "g3"] if is_running[x]]:
    out += "Server %s is running.\n" % g
    print "in loop: out = ", out

logger_log(log_dir, out)
logger_log(log_dir, '----------------------------------------------\n')



# if log_dir specified
if log_dir is not None:
	for i in range(0, len(data_dirs)):
		os.system('mv ' + out[i]  + ' ' + os.path.join(log_dir, 'log-'+str(i)))

# os.system('docker rm $(docker stop -t 0 $(docker ps -aq)) > /dev/null')

os.system('docker rm $(docker stop -t 0 $(docker ps -aq)) > /dev/null')
#time.sleep(5)
