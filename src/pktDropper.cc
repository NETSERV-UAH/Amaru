#include <string.h>
#include <omnetpp.h>

using namespace omnetpp;

class pktDropper : public cSimpleModule
{
  private:
    simtime_t dropStartTime=0;
    simtime_t dropEndTime=0; //Keep track of AMACs learned so far
    bool shouldDropPacket=false;
    int failureDetectionDelay=0;
    bool isDropping=false;
    bool isRestored=false;
  protected:
    // The following redefined virtual function holds the algorithm.
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;
    virtual void finish() override;
};
// The module class needs to be registered with OMNeT++
Define_Module(pktDropper);
void pktDropper::initialize()
{
    dropStartTime=par("dropStartTime");
    dropEndTime=par("dropEndTime");
    shouldDropPacket=par("shouldDropPacket");
    failureDetectionDelay=par("failureDetectionDelay");
}
void pktDropper::handleMessage(cMessage *msg)
{
    std::cout<<"Message arrived. Node:  "<<getName()<<" Message Type: "<<msg->getName()<<std::endl;
    if(strcmp(msg->getName(),"failureNotificationLoopMsg")==0)
    {
        cMessage *msg = new cMessage("Failure");
        send(msg, "port$o", 0);
        send(msg, "port$o", 1);
    }
    else
    {
        int arrivalPort=msg->getArrivalGate()->getIndex();
        int nextHop=(arrivalPort==0?1:0);
        if(shouldDropPacket==false||SimTime()<dropStartTime||SimTime()>dropEndTime)
        {
            send(msg, "port$o", nextHop);
        }
        else
        {
            if(isDropping==false)
            {
                isDropping=true;
                cMessage *msg = new cMessage("failureNotificationLoopMsg");          
                scheduleAt(dropStartTime+failureDetectionDelay, msg);
            }
            delete msg;
        }
    }
}
void pktDropper::finish()
{
}
