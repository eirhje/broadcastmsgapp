# simpleudp.tcl Simple UDP listener script for eggdrop by eirik@blix.com
# dependency: apt-get install tcl-udp
package require udp

# Change this to the channel you want this script to work on.
set our_chan "#sleipnir"
set udp_listen_port "5555"

# When receiving an UDP datagram, relay it to $our_chan
proc udpEventHandler sock {
    global our_chan
    # To get more info of the sender, use: set peer [udp_conf $sock -peer]
    putserv "privmsg $our_chan :[read $sock]"
    return 1
}

# Prevent binding two times, e.g. with .rehash or on SIGHUP
if {[info exists srv]==0} {
    # Setup the UDP socket listener, and send events to the eventHandler
    set srv [udp_open $udp_listen_port]
    fileevent $srv readable [list ::udpEventHandler $srv]
}
