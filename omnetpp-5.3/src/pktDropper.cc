#include <string.h>
#include <omnetpp.h>

using namespace omnetpp;
//This class is designed to support simulation of network reconfiguration. This is not part of the Amaru protocol.
class pktDropper : public cSimpleModule
{
  private:
    simtime_t dropStartTime;
    double dropDuration; //Keep track of AMACs learned so far
    bool shouldDropPacket;
    double failureDetectionDelay;
    bool isDropping=false;
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
    dropDuration=par("dropDuration");
    shouldDropPacket=par("shouldDropPacket");
    failureDetectionDelay=par("failureDetectionDelay");
    
    if(shouldDropPacket&&dropStartTime>=0)
    {
        cMessage *msg = new cMessage("packetDropStartLoopMsg");          
        scheduleAt(dropStartTime, msg);
        if(dropDuration>0)//Zero drop duration will drop packets indefinitely
        {
            cMessage *msg = new cMessage("packetDropEndLoopMsg");          
            scheduleAt(dropStartTime+dropDuration, msg);                        
        }
        
        if(failureDetectionDelay>=0)//zero detection delay will immediately notify about failure
        {
            cMessage *msg = new cMessage("failureNotificationLoopMsg");          
            scheduleAt(dropStartTime+failureDetectionDelay, msg);
            if(dropDuration>0)//Nofitication of restore
            {
                cMessage *msg = new cMessage("restoreNotificationLoopMsg");          
                scheduleAt(dropStartTime+dropDuration+failureDetectionDelay, msg);                        
            }
        }
    }
}

void pktDropper::handleMessage(cMessage *msg)
{
    std::cout<<"Message arrived. Node:  "<<getName()<<" Message Type: "<<msg->getName()<<std::endl;
    if(strcmp(msg->getName(),"failureNotificationLoopMsg")==0)
    {
        cMessage *msg1 = new cMessage("LinkFailure");//Notify adjacent nodes of link failure
        send(msg1, "port$o", 0);//notify failure in both direction
        send(msg1->dup(), "port$o", 1);
        delete msg;
    }
    else if(strcmp(msg->getName(),"restoreNotificationLoopMsg")==0)
    {
        //cMessage *msg2 = new cMessage("LinkRestore");//Notify adjacent nodes of link failure
        //send(msg2, "port$o", 0);//notify failure in both direction
        //send(msg2->dup(), "port$o", 1);
        //delete msg;
    }
    else if(strcmp(msg->getName(),"packetDropStartLoopMsg")==0)
    {
        isDropping=true;
        std::cout<<"Set isDropping to true"<<std::endl;
        delete msg;
        std::cout<<"Loopback message deleted"<<std::endl;
    }
    else if(strcmp(msg->getName(),"packetDropEndLoopMsg")==0)
    {
        isDropping=false;
        delete msg;
    }
    else
    {
        int arrivalPort=msg->getArrivalGate()->getIndex();
        int nextHop=(arrivalPort==0?1:0);//get opposite direction of the packet arrival
        if(isDropping==false)
        {
            send(msg, "port$o", nextHop);//forward packet towards the opposite direction
        }
        else
        {
            delete msg;//drop packet
        }
    }
}
void pktDropper::finish()
{
}
