# Amaru
Amaru: Guaranteed resiliency for in-band control in SDN

## Building and running simulation on Ubuntu 18.04:

1. Become superuser

> $ su

1. cd to src directory

> \# cd /home/user/Amaru/src (change /home/user/Amaru/src according to your src path)

1. Ensure that OMNeT++ bin directory is included in $PATH

> \# export PATH=/home/user/omnetpp/bin:$PATH (change /home/user/omnetpp/bin according to your OMNeT++ bin directory path)

1. make

> \# make

1. Run the simulation

> \# ./Amaru -u Cmdenv -n ../simulations:. -f ../simulations/omnetpp.ini
