docker run -v /home/me/wss/ws1/etc/glusterfs:/etc/glusterfs:z \
-v /home/me/wss/ws1/var/lib/glusterd:/var/lib/glusterd:z -v \
/home/me/wss/ws1/var/log/glusterfs:/var/log/glusterfs:z -v \
/sys/fs/cgroup:/sys/fs/cgroup:ro \
-d --privileged=true --net=host \
-v /dev/:/dev gluster/gluster-fedora


#docker stop $(docker ps -a -q)
#docker rm $(docker ps -a -q)

docker network create netgfs

# single
docker run  --name g1 --net netgfs -v /home/me/wss/ws1/etc/glusterfs:/etc/glusterfs:z \
-v /home/me/wss/ws1/var/lib/glusterd:/var/lib/glusterd:z -v \
/home/me/wss/ws1/var/log/glusterfs:/var/log/glusterfs:z -v \
/sys/fs/cgroup:/sys/fs/cgroup:ro \
-d --privileged=true \
-v /dev/:/dev gluster/gluster-fedora


# g1
docker run  --name g1 --net netgfs -v /home/me/wss/g1/etc/glusterfs:/etc/glusterfs:z \
-v /home/me/wss/g1/var/lib/glusterd:/var/lib/glusterd:z -v \
/home/me/wss/g1/var/log/glusterfs:/var/log/glusterfs:z -v \
/sys/fs/cgroup:/sys/fs/cgroup:ro \
-d --privileged=true \
-v /home/me/wss/g1/data/gv0:/mnt/gv0 \
gluster/gluster-fedora

# g2
docker run  --name g2 --net netgfs -v /home/me/wss/g2/etc/glusterfs:/etc/glusterfs:z \
-v /home/me/wss/g2/var/lib/glusterd:/var/lib/glusterd:z -v \
/home/me/wss/g2/var/log/glusterfs:/var/log/glusterfs:z -v \
/sys/fs/cgroup:/sys/fs/cgroup:ro \
-d --privileged=true \
-v /home/me/wss/g2/data/gv0:/mnt/gv0 \
 gluster/gluster-fedora

# g3
docker run  --name g3 --net netgfs -v /home/me/wss/g3/etc/glusterfs:/etc/glusterfs:z \
-v /home/me/wss/g3/var/lib/glusterd:/var/lib/glusterd:z -v \
/home/me/wss/g3/var/log/glusterfs:/var/log/glusterfs:z -v \
/sys/fs/cgroup:/sys/fs/cgroup:ro \
-d --privileged=true \
-v /home/me/wss/g3/data/gv0:/mnt/gv0 \
 gluster/gluster-fedora


# docker ps -a
# docker inspect <id>
# docker exec -ti <id> bash
# ps aux |grep glusterd

gluster peer status
gluster --version

# from each server probe others
gluster peer probe g1.netgfs
gluster peer probe g2.netgfs
gluster peer probe g3.netgfs

gluster peer status
gluster pool list

# Create volumes
gluster volume create gv0 replica 3 g1:/mnt/gv0/v g2:/mnt/gv0/v g3:/mnt/gv0/v
gluster volume start gv0
gluster volume info gv0
# mounting back
mount -t glusterfs g1:/gv0 /mnt/m
for i in `seq -w 1 100`; do cp -rp /var/log/messages /mnt/m/copy-test-$i; done

#First, check the client mount point:

# ls -lA /mnt/copy* | wc -l

You should see 100 files returned. Next, check the GlusterFS brick mount points on each server:

# ls -lA /data/brick1/gv0/copy*

You should see 100 files on each server using the method we listed here. Without replication, in a distribute only volume (not detailed here), you should see about 33 files on each one.

# gluster s3
docker pull gluster/gluster-s3

docker run -d --privileged  \
--net netgfs \
--name s3 \
-v /sys/fs/cgroup/:/sys/fs/cgroup/:ro -p 8080:8080 \
-v /home/me/wss/ws1/mnt/gluster-object:/mnt/gluster-object \
-e S3_ACCOUNT="tv1" -e S3_USER="admin" \
-e S3_PASSWORD="redhat" \
gluster/gluster-s3


curl -i -X PUT http://localhost:8080/v1/AUTH_myvolume/mycontainer

curl -v -H 'X-Storage-User: tv1:admin' -H 'X-Storage-Pass: redhat' \
-k http://localhost:8080/auth/v1.0

