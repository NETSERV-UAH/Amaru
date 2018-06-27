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
    int numberOfLearnedAMACs=0; //Keep track of AMACs learned so far
    bool isARoot;
    int N=3; //Max number of AMACs - When a switch reaches this number (if set to nonzero), it starts discarding new frames and does not learn anymore.
    int L=3; //L: Preffix variation length - learn the N (if set to nonzero) first that vary in the prefix of length L
    static const int depth=16;
    static const int breadth=8;
    struct AMAC
    {
        int level;
        int octets[depth];
    };
    /*struct AMACList
    {
        std::vector<AMAC> amacList;
    };*/
    std::vector<AMAC> *portAMACListArray[breadth];//Store list of AMACs for each port
  protected:
    // The following redefined virtual function holds the algorithm.
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;
    virtual void finish() override;
    virtual void broadcastAFrameAsRoot(int aRoot, int arrivalPort);
    virtual void broadcastAFrame(AMAC aMAC, int arrivalPort);
    virtual void processAFrame(int arrivalPort, AFrame* aFrame);
    virtual bool isLoopFreeAMAC(AMAC aMAC);
    virtual int getNextHopUpstream(AMAC aMAC);
    virtual void printAMAC(AMAC aMAC);
    virtual void printAllAMAC();
    virtual void printAMAC(AFrame* aFrame);
};
// The module class needs to be registered with OMNeT++
Define_Module(node);
void node::initialize()
{
    isARoot=false;
    numberOfPorts=gateSize("port$o");
    EV<<"Initialize: num ports "<<numberOfPorts<<"\n";
    std::cout<<"Initializing... switch: "<<getName()<<" number of ports: "<<numberOfPorts<<std::endl;
    for(int i=0;i<breadth;i++)
    {
        portAMACListArray[i]=nullptr;
    }
    
    if(strcmp(getName(),"s9")==0)//test S2C message; will be moved from here
    {            
        AFrame* aFrame1=new AFrame("S2C");
        aFrame1->setLevel(5);
        aFrame1->setAMAC(0,0);
        aFrame1->setAMAC(1,1);
        aFrame1->setAMAC(2,2);
        aFrame1->setAMAC(3,1);
        aFrame1->setAMAC(4,2);            
        scheduleAt(10, aFrame1);                    
    }
}
void node::handleMessage(cMessage *msg)
{    
    std::cout<<"Message arrived. Node:  "<<getName()<<" Message Type: "<<msg->getName()<<std::endl;
    int arrivalPort;
    try{
        if(strcmp(msg->getName(),"S2C")!=0)
            arrivalPort=msg->getArrivalGate()->getIndex();
    }catch(...)
    {
    }
    
    AFrame* aFrame=(AFrame*)msg;

    if(strcmp(msg->getName(),"CoI")==0)//Directly connected to an SDN Controller
    {
        isARoot=true;
        int receivedAMAC=aFrame->getAMAC(0);
        AMAC aMAC;
        aMAC.level=1;
        aMAC.octets[0]=receivedAMAC;
        std::cout<<"AMAC is "<<receivedAMAC<<" from SDN Controller for port "<<arrivalPort<<"\n";

        if(portAMACListArray[arrivalPort]==nullptr)
        {
            portAMACListArray[arrivalPort]=new std::vector<AMAC>();
        }
        portAMACListArray[arrivalPort]->push_back(aMAC);
        broadcastAFrameAsRoot(receivedAMAC, arrivalPort);
        delete msg;
    }
    else if(strcmp(msg->getName(),"AMAC")==0)
    {
        std::cout<<"AMAC received for port "<<arrivalPort<<"\n";
        printAMAC(aFrame);
        processAFrame(arrivalPort, aFrame);
    }
    else if(strcmp(msg->getName(),"S2C")==0)
    {     
        AMAC aMAC1;
	int receivedLevel=aFrame->getLevel();
	aMAC1.level=receivedLevel;
	for(int i=0;i<receivedLevel;i++)//Copy octets
	{
		aMAC1.octets[i]=aFrame->getAMAC(i);
	}
        int nextHop = getNextHopUpstream(aMAC1);
        //std::cout<<"S2C message arrived at "<<getName()<<": sending AFrame with AMAC ";
        //printAMAC(aMAC1);
        //std::cout<<" to port "<<nextHop<<std::endl;
        send(aFrame, "port$o", nextHop);
    }
}

bool node::isLoopFreeAMAC(AMAC aMAC)
{
    bool amacIsLoopFree=true;
    for(int i=0;i<breadth;i++)//check AMAClist of each port to see if received AMAC was originated from this switch
    {
        if(portAMACListArray[i]!=nullptr)
        {
            std::vector<AMAC> *portAMACList=portAMACListArray[i];
            for(int j=0;j<portAMACList->size();j++)//check all AMAC associated with this port
            {
                AMAC portAMAC=portAMACList->at(j);
                if(portAMAC.level<=aMAC.level)
                {
                    bool prefixMatch=true;
                    int maxSearchLevel=(L==0?portAMAC.level:L);
                    for(int k=0;k<maxSearchLevel;k++)
                    {
                        if(portAMAC.octets[k]!=aMAC.octets[k])
                        {
                            prefixMatch=false;
                            break;
                        }
                    }
                    if(prefixMatch)
                    {
                        amacIsLoopFree=false;
                        std::cout<<"AMAC ";
                        printAMAC(aMAC);
                        std::cout<<"not loop free. Originated from ";
                        printAMAC(portAMAC);
                        std::cout<<std::endl;
                    }
                }
            }
        }
    }
    return amacIsLoopFree;
}

void node::printAMAC(AMAC aMAC)
{
    for(int i=0;i<aMAC.level;i++)
    {
        std::cout<<aMAC.octets[i]<<".";
    }
    //std::cout<<std::endl;
}

void node::printAMAC(AFrame *aFrame)
{
    for(int i=0;i<aFrame->getLevel();i++)
    {
        std::cout<<aFrame->getAMAC(i)<<".";
    }
    //std::cout<<std::endl;
}

void node::printAllAMAC()
{
    for(int i=0;i<breadth;i++)//check AMAClist of each port to see if received AMAC was originated from this switch
    {
        if(portAMACListArray[i]!=nullptr)
        {
            std::cout<<"\tPort "<<i<<std::endl;
            std::vector<AMAC> *portAMACList=portAMACListArray[i];
            for(int j=0;j<portAMACList->size();j++)//check all AMAC associated with this port
            {
                std::cout<<"\t\tAMAC "<<j<<": ";
                AMAC portAMAC=portAMACList->at(j);
                printAMAC(portAMAC);
                std::cout<<std::endl;
            }
        }
    }    
}

int node::getNextHopUpstream(AMAC aMAC)
{
    int nextHopUpstream=-1;
    std::cout<<"getNextHopUpstream. Got AMAC ";
    printAMAC(aMAC);
    std::cout<<std::endl;
    for(int i=0;i<breadth;i++)//check AMAClist of each port to see if received AMAC was originated from this switch
    {
        if(portAMACListArray[i]!=nullptr)
        {
            std::vector<AMAC> *portAMACList=portAMACListArray[i];
            for(int j=0;j<portAMACList->size();j++)//check all AMAC associated with this port
            {
                AMAC portAMAC=portAMACList->at(j);
                //std::cout<<"Matching with port AMAC ";
                //printAMAC(portAMAC);
                //std::cout<<std::endl;
                if(portAMAC.level<=aMAC.level)//both level will be equal only in case of self message, otherwise port level will be less than message level
                {
                    bool prefixMatch=true;                    
                    for(int k=0;k<portAMAC.level;k++)
                    {
                        if(portAMAC.octets[k]!=aMAC.octets[k])
                        {
                            prefixMatch=false;
                            break;
                        }
                    }
                    if(prefixMatch)
                    {
                        nextHopUpstream=i;
                        std::cout<<"Next upstream hop for AMAC ";
                        printAMAC(aMAC);
                        std::cout<<"is "<<nextHopUpstream<<std::endl;                        
                    }
                }
            }
        }
    }
    return nextHopUpstream;
}

void node::processAFrame(int arrivalPort, AFrame* aFrame)
{
	AMAC aMAC;
	int receivedLevel=aFrame->getLevel();
	aMAC.level=receivedLevel;
	for(int i=0;i<receivedLevel;i++)//Copy octets
	{
		aMAC.octets[i]=aFrame->getAMAC(i);
	}
	bool amacIsLoopFree=isLoopFreeAMAC(aMAC);//Check if AMAC is loop free
	if(amacIsLoopFree)
	{
            if(N<=0 || numberOfLearnedAMACs<N)
            {
                if(portAMACListArray[arrivalPort]==nullptr)
                {
                    portAMACListArray[arrivalPort]=new std::vector<AMAC>();
                }
                portAMACListArray[arrivalPort]->push_back(aMAC);//add AMAC to port
                numberOfLearnedAMACs++;
                if(aMAC.level<depth)
                    broadcastAFrame(aMAC, arrivalPort);//Send out to all ports except the receiving port
            }
            else
            {
                std::cout<<"Not learning due to max number of AMAC ("<<N<<") already learned."<<std::endl;
            }
	}
	else
	{
	    std::cout<<"Discarding loop AMAC"<<std::endl;
	}
	delete aFrame;
}

void node::broadcastAFrameAsRoot(int aRoot, int arrivalPort)
{
    for(int i=0;i<numberOfPorts;i++)
    {
        if(i!=arrivalPort)
        {
            AFrame* aFrame=new AFrame("AMAC");
            aFrame->setLevel(2);
            aFrame->setAMAC(0,aRoot);
            aFrame->setAMAC(1,i);
            send(aFrame, "port$o", i);
        }
    }
}

void node::broadcastAFrame(AMAC aMAC, int arrivalPort)
{
    //std::cout<<"Number of ports: "<<numberOfPorts<<std::endl;
    for(int i=0;i<numberOfPorts;i++)
    {
        if(i!=arrivalPort)
        {
            AFrame* aFrame=new AFrame("AMAC");
            aFrame->setLevel(aMAC.level+1);//Increment level by 1

            for(int j=0;j<aMAC.level;j++)
            {
                aFrame->setAMAC(j,aMAC.octets[j]);//Copy received AMAC
            }
            aFrame->setAMAC(aMAC.level,i);//Append this port identifier to received AMAC before sending out
            send(aFrame, "port$o", i);
        }
    }
}

void node::finish()
{
    std::cout<<"Printing AMAC list for node "<<getName()<<std::endl;
    printAllAMAC();
    for(int i=0;i<breadth;i++)//free allocated memory for AMAC list from each port
    {
        if(portAMACListArray[i]!=nullptr)
        {
            //delete portAMACListArray[i];
           // portAMACListArray[i]=nullptr;
        }
    }
}
