#include <string.h>
#include <omnetpp.h>
using namespace omnetpp;
class pktgen : public cSimpleModule
{
  protected:
    // The following redefined virtual function holds the algorithm.
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;
};
// The module class needs to be registered with OMNeT++
Define_Module(pktgen);
void pktgen::initialize()
{
    EV<<"Generating packet \n";
    cMessage *msg = new cMessage("loopMsg");
    send(msg, "port$o");
}
void pktgen::handleMessage(cMessage *msg)
{
    // The handleMessage() method is called whenever a message arrives
    // at the module. Here, we just send it to the other module, through
    // gate `out'. Because both `tic' and `toc' does the same, the message
    // will bounce between the two.
    EV<<"PKTGEN "<<msg<<"\n";
}
