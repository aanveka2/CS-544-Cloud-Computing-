#!/usr/bin/python3
import unshare
import argparse
import os
import sys 


def uts_namespace(args):
    try:
        unshare.unshare(unshare.CLONE_NEWUTS)
    except:
        print("The calling process doesnot have a private copy of UTS namespace")

    os.system("hostname %s" % args.hostname)
    

def net_namespace(args):
    try:
        unshare.unshare(unshare.CLONE_NEWNET)
    except:
        print("The calling process was not moved in new network namespace")

    os.system("ip link add dummy1 type dummy")
    os.system("ip link set name eth0 dev dummy1")
    os.system("ifconfig eth0 %s" % args.ip_addr)

def mnt_namespace(args):
    try:
        unshare.unshare(unshare.CLONE_NEWUTS)
    except:
        print("The calling process doesnot have a private copy of UTS namespace")

    
    os.chdir(args.root_path)
    os.chroot(".")
    #os.system('mount -t proc proc /proc')

def pid_namespace(args):
    try:
        unshare.unshare(unshare.CLONE_NEWPID)
    except:
        print("The calling process doesnot have a new copy of PID namespace")
        

def cpu_cgroup(args):
    os.system('mount -t sysfs sysfs /sys')
    os.system('mount -t tmpfs cgroup_root /sys/fs/cgroup')
    os.system('mkdir /sys/fs/cgroup/cpuset')
    os.system('mount -t cgroup cpuset -o cpuset /sys/fs/cgroup/cpuset/')
    os.system(f"mkdir /sys/fs/cgroup/cpuset/group1")
    os.system(f'echo 0 > /sys/fs/cgroup/cpuset/group1/cpuset.cpus')
    os.system(f'echo 0 > /sys/fs/cgroup/cpuset/group1/cpuset.mems')
    
    
    


def mem_cgroup(args):
    os.system('mount -t sysfs sysfs /sys')
    os.system('mount -t tmpfs cgroup_root /sys/fs/cgroup')
    os.system('mkdir /sys/fs/cgroup/memory')
    os.system('mount -t cgroup memory -o memory /sys/fs/cgroup/memory/')
    os.system('mkdir /sys/fs/cgroup/memory/group1')
    os.system('echo $$ > /sys/fs/cgroup/memory/group1/tasks')
    os.system('echo 10M > /sys/fs/cgroup/memory/group1/memory.limit_in_bytes')
    

def exe_bash(args):
    newpid = os.fork()
    
    if newpid == 0:
        os.system('mount -t proc proc /proc')
        os.execle('/bin/bash', '/bin/bash', os.environ)
    else:
        os.wait()
        os.system('umount /sys/fs/cgroup/cpuset')
        os.system('umount /sys/fs/cgroup')
        os.system('umount /sys')
        os.system('umount /proc')
    pass





if __name__ == "__main__":
    print ("*************************")
    print ("*                       *")
    print ("*      Mini Docker      *")
    print ("*                       *")
    print ("*************************")

    parser = argparse.ArgumentParser(description='This is a miniDocker.')

    parser.add_argument('--hostname', action="store", dest="hostname", type=str, default="administrator",
                    help='set the container\'s hostname')

    parser.add_argument('--ip_addr', action="store", dest="ip_addr", type=str, default="10.0.0.1",
                    help='set the container\'s ip address')

    parser.add_argument('--mem', action="store", dest="mem_size", type=int, default=10,
                    help='set the container\'s memory size (MB)')

    parser.add_argument('--cpu', action="store", dest="cpu_num", type=int, default=1,
                    help='set the container\'s cpu number')

    parser.add_argument('--root_path', action="store", dest="root_path", type=str, default="./new_root",
                    help='set the new root file system path of the container')
    
    args = parser.parse_args()



    #create hostname namespace
    uts_namespace(args)
    #create network namespace
    net_namespace(args)
    #create filesystem namespace
    mnt_namespace(args)
    #create cpu cgroup
    cpu_cgroup(args)
    #create memory cgroup
    mem_cgroup(args)
    #create pid namespace
    pid_namespace(args)
    #execute the bash process "/bin/bash"
    exe_bash(args)
