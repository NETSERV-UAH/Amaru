//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
// 
// You should have received a copy of the GNU Lesser General Public License
// along with this program.  If not, see http://www.gnu.org/licenses/.
// 

package amaru.simulations;

import amaru.node;
import amaru.pktDropper;
import amaru.pktgen;
import amaru.sdnController;


network Figure1
{
    @display("bgb=428,387");
    submodules:
        sdnController: sdnController {
            @display("p=71,50");
        }
        s1: node {
            @display("p=71,120");
        }
        s2: node {
            @display("p=183,120");
        }
        s3: node {
            @display("p=284,120");
        }
        s4: node {
            @display("p=71,202");
        }
        s5: node {
            @display("p=183,202");
        }
        s6: node {
            @display("p=284,202");
        }
        s7: node {
            @display("p=71,290");
        }
        s8: node {
            @display("p=183,290");
        }
        s9: node {
            @display("p=317,304");
        }
        pktDropper6_9: pktDropper {
            @display("p=349,236");
        }
        pktDropper8_9: pktDropper {
            @display("p=252,336");
        }
        pktgen: pktgen {
            @display("p=388,336");
        }
    connections:
        sdnController.port++ <--> {  delay = 1s; } <--> s1.port++;
        s1.port++ <--> {  delay = 1s; } <--> s2.port++;
        s2.port++ <--> {  delay = 1s; } <--> s3.port++;
        s4.port++ <--> {  delay = 1s; } <--> s5.port++;
        s5.port++ <--> {  delay = 1s; } <--> s6.port++;
        s7.port++ <--> {  delay = 1s; } <--> s8.port++;
        s8.port++ <--> {  delay = 1s; } <--> pktDropper8_9.port++;
        s9.port++ <--> {  delay = 1s; } <--> pktDropper8_9.port++;
        s1.port++ <--> {  delay = 1s; } <--> s4.port++;
        s4.port++ <--> {  delay = 1s; } <--> s7.port++;
        s2.port++ <--> {  delay = 1s; } <--> s5.port++;
        s5.port++ <--> {  delay = 1s; } <--> s8.port++;
        s3.port++ <--> {  delay = 1s; } <--> s6.port++;
        s6.port++ <--> {  delay = 1s; } <--> pktDropper6_9.port++;
        s9.port++ <--> {  delay = 1s; } <--> pktDropper6_9.port++;
        s9.port++ <--> {  delay = 1s; } <--> pktgen.port;
}
