#!/usr/bin/python
import sys
from mininet.topo import Topo
from mininet.node import OVSSwitch
from mininet.node import OVSController

class OVSBridgeSTP(OVSSwitch):
    prio = 1000
    def start(self, *args, **kwargs):
        OVSSwitch.start(self, *args, **kwargs)
        OVSBridgeSTP.prio += 1
        self.cmd('ovs-vsctl set-fail-mode', self, 'standalone')
        self.cmd('ovs-vsctl set-controller', self)
        self.cmd('ovs-vsctl set Bridge', self, 'stp_enable=true', 'other_config:stp-priority=%d' % OVSBridgeSTP.prio)

switches = {'ovs-stp': OVSBridgeSTP}

class clos(Topo):
    def __init__(self, numberOfLeafs, numberOfSpines, *args, **kwargs):
        Topo.__init__(self, *args, **kwargs)
        hosts, leafs, spines, dpid = {},{}, {}, 0 
        for i in range(0, numberOfLeafs - 1):
            loc = '%dx' % (i + 1)
            host = hosts[i] = self.addHost('h' + loc)
            leaf = leafs[i] = self.addSwitch('l' + loc)
        for j in range (0, numberOfSpines - 1):
            loc = '%dx' % (i + 1)
            spine = spines[i, j] = self.addSwitch('s' + loc)
        for i in range(0, numberOfLeafs - 1):
            host = hosts[i]
            leaf = leafs[i]
            self.addLink(leaf, host)
            for j in range(0, numberOfSpines - 1):
                spine = spines[j]
                self.addLink(spine, leaf)

topos = { 'clos': clos}


