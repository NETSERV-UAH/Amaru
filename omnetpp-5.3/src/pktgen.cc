#include <string.h>
#include <omnetpp.h>
#include "AFrame_m.h"

using namespace omnetpp;
class pktgen : public cSimpleModule
{
private:
    long packetsSent;
    long packetsToSend;
    int packetDelay;
    double packetSendStartTime;
    cChiSquare chiSquare;
  protected:
    // The following redefined virtual function holds the algorithm.
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;
};
// The module class needs to be registered with OMNeT++
Define_Module(pktgen);
void pktgen::initialize()
{
    //cMessage *msg = new cMessage("S2C");
    packetsSent=0;
    packetsToSend=par("packetsToSend").longValue();
    packetDelay=par("packetDelay");
    packetSendStartTime=par("packetSendStartTime").doubleValue();

    //double chaos=getRNG(0)->doubleRand();
    AFrame* aFrame1=new AFrame("S2C");
    aFrame1->setLevel(-1);
    /*aFrame1->setAMAC(0,0);
    aFrame1->setAMAC(1,1);
    aFrame1->setAMAC(2,1);
    aFrame1->setAMAC(3,1);
    aFrame1->setAMAC(4,2);*/
    scheduleAt(packetSendStartTime,aFrame1);
}
void pktgen::handleMessage(cMessage *msg)
{
    // The handleMessage() method is called whenever a message arrives
    // at the module. Here, we just send it to the other module, through
    // gate `out'. Because both `tic' and `toc' does the same, the message
    // will bounce between the two.
    if(msg->isSelfMessage())
    {
        send(msg->dup(), "port$o");
        packetsSent++;
        if(packetsSent<packetsToSend)
        {
            double chaos=getRNG(0)->doubleRand();
            scheduleAt(simTime()+chaos*10*packetDelay,msg->dup());
        }
    }
    delete msg;
}
