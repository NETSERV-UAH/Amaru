# Amaru
Amaru: Guaranteed resiliency for in-band control in SDN

Building and running simulation on Ubuntu 18.04:

1. Become superuser

$ su

2. cd to src directory

\# cd /home/user/Amaru/src (change /home/user/Amaru/src according to your src path)

2. Ensure that OMNeT++ bin directory is included in $PATH

\# export PATH=/home/user/omnetpp/bin:$PATH (change /home/user/omnetpp/bin according to your OMNeT++ bin directory path)

3. make

\# make

4. Run the simulation

\# ./Amaru -u Cmdenv -n ../simulations:. -f ../simulations/omnetpp.ini
