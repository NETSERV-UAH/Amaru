#include <string.h>
#include <omnetpp.h>
#include <algorithm>
#include <vector>
#include <math.h>
#include "AFrame_m.h"
using namespace omnetpp;

class node : public cSimpleModule
{
  private:
    int numberOfPorts;
    bool isARoot;
    struct AMAC
    {
        int level;
        int octets[6];
    };
    struct AMACList
    {
        std::vector<AMAC> amacList;
    };
    AMACList portAMACListArray[8];//Store list of AMACs for each port
  protected:
    // The following redefined virtual function holds the algorithm.
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;
    virtual void finish() override;
    virtual void broadcastAFrameAsRoot();
};
// The module class needs to be registered with OMNeT++
Define_Module(node);
void node::initialize()
{
    isARoot=false;
    numberOfPorts=gateSize("port$o");
    //Notify every connected nodes that they are connected directly to an SDN Controller
    /*for(int i=0; i<numberOfPorts; i++)
    {
        cMessage *msg = new cMessage("CoI");
        send(msg, "port$o", i);
    }*/
}
void node::handleMessage(cMessage *msg)
{
    EV<<"Message arrived "<<msg->getName()<<"\n";
    if(strcmp(msg->getName(),"CoI")==0)//Directly connected to an SDN Controller
    {
        isARoot=true;
        int arrivalPort=msg->getArrivalGate()->getIndex();

        broadcastAFrameAsRoot();
    }
}

void node::broadcastAFrameAsRoot()
{
    for(int i=0;i<numberOfPorts;i++)
    {
        AFrame* aFrame=new AFrame("AMAC");
        aFrame->setLevel(1);
        aFrame->setAMAC(0,i);
        send(aFrame, "port$0", i);
    }
}

void node::finish()
{
}
