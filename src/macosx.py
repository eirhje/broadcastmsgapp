#!/usr/bin/env python
import os
import sys
import socket

#START OPTIONS
bcast_port = 6000
bcast_ip = "172.31.0.255"
pidfile = "/tmp/broadcast.pid"
#END OPTIONS

print "Broadcast notify -- by Eirik H. Blix"
mysocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mysocket.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
mysocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print sys.argv[0]+" --help \tShow this help"
    print sys.argv[0]+"     \tStart the client"
        print sys.argv[0]+" \"message\" \tBroadcast message and exit"
        print sys.argv[0]+" --stop      \tStop the client"

        sys.exit(0)

if len(sys.argv) > 1 and sys.argv[1] == "--stop":
    pid = open(pidfile).read()
    os.kill(int(pid),9)
    print "Sent kill message to pid "+str(pid)
    os.unlink(pidfile)
    sys.exit(0)

if len(sys.argv) > 1:
    message = ""
    for text in sys.argv[1:]:
        message = message+text+" "
    mysocket.sendto(message,(bcast_ip,bcast_port))
    sys.exit(0)

# No options, most likely wants clientmode

try:
    open(pidfile).read()
    print "Already running client..."
except:
    pid = os.fork()
    if pid:
        print sys.argv[0]+" started with pid: "+str(pid)
        f = open(pidfile,'w')
        f.write(str(pid))
        f.close()
        os.system("osascript -e 'tell app \"System Events\" to display notification \"Started Broadcast App\" with title \"Broadcast\" subtitle \"Eirik H. Blix\"'")
        sys.exit(0)
    else:
        mysocket.bind((bcast_ip, bcast_port))
        while 1:
            data = mysocket.recv(1024)
            os.system("osascript -e 'tell app \"System Events\" to display notification \""+data+"\" with title \"PBX\" subtitle \"Eirik H. Blix\"'")
