#include <string.h>
#include <omnetpp.h>
#include <algorithm>
#include <vector>
#include <math.h>
#include "AFrame_m.h"
using namespace omnetpp;

class sdnController : public cSimpleModule
{
  protected:
    // The following redefined virtual function holds the algorithm.
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;
    virtual void finish() override;
};
// The module class needs to be registered with OMNeT++
Define_Module(sdnController);
void sdnController::initialize()
{
    int numberOfPorts=gateSize("port$o");
    //Notify every connected nodes that they are connected directly to an SDN Controller
    for(int i=0; i<numberOfPorts; i++)
    {
        AFrame *aFrame = new AFrame("CoI");
        std::cout<<"I am the SDN Controller. Sending out CoI through port: "<<i<<"\n";
        aFrame->setLevel(1);
        aFrame->setAMAC(0,i);
        send(aFrame, "port$o", i);
    }
}
void sdnController::handleMessage(cMessage *msg)
{
    delete msg;
}

void sdnController::finish()
{
}
