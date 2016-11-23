#!/bin/bash

if [ "$1" == "3" ] ; then
    sudo ./clos3.py 3 3
else
    sudo mn --custom clos3.py --topo clos,numberOfLeafs=3,numberOfSpines=3
fi
