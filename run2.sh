#!/bin/bash

if [ "$1" == "3" ] ; then
    sudo ./clos2.py 3 3
else
    sudo mn --custom clos2.py --switch ovs-stp --topo clos,numberOfLeafs=3,numberOfSpines=3
fi
