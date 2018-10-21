#### How to use different topologies in an OMNeT++ simulation in the same project?

Use the omnetpp.ini or your project .ini file to create different scenario. Now, you can use different topologies for each scenario.

In the following example we are setting two different topologies (tolology1.ned topology2.ned) in two different scenario.

Example:-
```
#Scenario-1
[Config Scenario1]
network=topology1

#Scenario-2
[Config Scenario2]
network=topology2
```
