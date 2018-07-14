#include <string.h>
#include <omnetpp.h>
#include <algorithm>
#include <vector>
#include <math.h>
#include "AFrame_m.h"
using namespace omnetpp;

class sdnController : public cSimpleModule
{
private:
    cOutVector recvVector;
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
    
    //send test C2S message: will be moved from here
    /*AFrame* aFrame1=new AFrame("C2S");
    aFrame1->setLevel(4);
    aFrame1->setAMAC(0,0);
    aFrame1->setAMAC(1,2);
    aFrame1->setAMAC(2,2);
    aFrame1->setAMAC(3,0);                
    sendDelayed(aFrame1, 20, "port$o", 0);*/
}
void sdnController::handleMessage(cMessage *msg)
{
    if(strcmp(msg->getName(),"S2C")==0)
    {
        recvVector.record(simTime()/100);
    }
    delete msg;
}

void sdnController::finish()
{
}
