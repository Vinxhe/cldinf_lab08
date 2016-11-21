#!/bin/bash

if [ "$1" == "3" ] ; then
    sudo ./clos.py 3 3
else
    sudo mn --custom clos.py --topo clos,numberOfLeafs=3,numberOfSpines=3
fi
