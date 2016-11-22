#!/usr/bin/python
import sys
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import OVSSwitch
from mininet.node import Controller, OVSController
from mininet.util import dumpNodeConnections

class STPSwitch(OVSSwitch):
    prio = 1000
    def start(self, *args, **kwargs):
        OVSSwitch.start(self, *args, **kwargs )
        STPSwitch.prio += 1
        self.cmd ('ovs-vsctl set-fail-mode', self, 'standalone')
        self.cmd('ovs-vsctl set Bridge', self, 'stp_enable=true', 'other_config:stp-priority=%d' % STPSwitch.prio)

switches = {'ovs-stp': STPSwitch}

class clos(Topo):
    def __init__(self, numberOfLeafs, numberOfSpines, *args, **kwargs):
        Topo.__init__(self, *args, **kwargs)

        spines = self.create(self.addSwitch, "spine", numberOfSpines, False)
        leafs = self.create(self.addSwitch, "leaf", numberOfLeafs, False)
        hosts = self.create(self.addHost, "host", numberOfLeafs, True)
	self.link(spines, leafs, hosts)

    def create(self, func, prefix, numberOfDevices, routed):
        devices = list()  
        for i in range(0, numberOfDevices):
            if (routed == True):
                devices.append (func(prefix + str(i + 1), ip='10.0.0.' + str(i + 1)))
            else:
                devices.append(func(prefix + str(i + 1), cls=STPSwitch))
        return devices

    def link(self, spines, leafs, hosts):
        index = 0
        for leaf in leafs:
            host = hosts[index]
            self.addLink(leaf, host)
            index += 1
            for spine in spines:
                self.addLink(leaf, spine)

topos = { 'clos': clos}

def initWithParams(numberOfSpines, numberOfLeafs):
    topo = clos(numberOfSpines, numberOfLeafs)
    net = Mininet(topo=topo, switch=STPSwitch)
    net.start()
    dumpNodeConnections(net.values())
    CLI(net)
    net.stop()

if __name__ == '__main__':
    initWithParams(int(sys.argv[1]), int(sys.argv[2]))
