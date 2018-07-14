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
network topology_rogers_ca
{
    @display("bgb=2213.64,1002.32996,#FFFFFF,#FFFFFF;bgl=51");
    types:
    submodules:

        pktDropper_Victoria_Vancouver: pktDropper {
            @display("i=abstract/opticalswitch_vs;p=286.38,119.97");
        }
        pktDropper_Victoria_Seattle: pktDropper {
            @display("i=abstract/opticalswitch_vs;p=25.154999,236.06999");
        }
        pktDropper_Vancouver_Seattle: pktDropper {
            @display("i=abstract/opticalswitch_vs;p=296.055,387");
        }
        pktDropper_Vancouver_Edmonton: pktDropper {
            @display("i=abstract/opticalswitch_vs;p=613.395,92.88");
        }
        pktDropper_Vancouver_Calgary: pktDropper {
            @display("i=abstract/opticalswitch_vs;p=630.81,286.38");
        }
        pktDropper_Edmonton_Calgary: pktDropper {
            @display("i=abstract/opticalswitch_vs;p=688.86,183.825");
        }
        pktDropper_Edmonton_Saskatoon: pktDropper {
            @display("i=abstract/opticalswitch_vs;p=864.945,30.96");
        }
        pktDropper_Calgary_Regina: pktDropper {
            @display("i=abstract/opticalswitch_vs;p=797.22,390.87");
        }
        pktDropper_Saskatoon_Winnipeg: pktDropper {
            @display("i=abstract/opticalswitch_vs;p=1027.485,145.125");
        }
        pktDropper_Regina_Winnipeg: pktDropper {
            @display("i=abstract/opticalswitch_vs;p=1031.355,267.03");
        }
        pktDropper_Winnipeg_Thunderbay: pktDropper {
            @display("i=abstract/opticalswitch_vs;p=1203.57,143.19");
        }
        pktDropper_Winnipeg_Minneapolis: pktDropper {
            @display("i=abstract/opticalswitch_vs;p=1267.4249,321.21");
        }
        pktDropper_Thunderbay_Sudbury: pktDropper {
            @display("i=abstract/opticalswitch_vs;p=1373.85,168.345");
        }
        pktDropper_Minneapolis_Milwaukee: pktDropper {
            @display("i=abstract/opticalswitch_vs;p=1424.16,356.04");
        }
        pktDropper_Sudbury_Toronto: pktDropper {
            @display("i=abstract/opticalswitch_vs;p=1538.325,170.28");
        }
        pktDropper_Milwaukee_Chicago: pktDropper {
            @display("i=abstract/opticalswitch_vs;p=1582.83,417.96");
        }
        pktDropper_Toronto_Ottawa: pktDropper {
            @display("i=abstract/opticalswitch_vs;p=1414.485,81.27");
        }
        pktDropper_Ottawa_Montreal: pktDropper {
            @display("i=abstract/opticalswitch_vs;p=1538.325,52.245");
        }
        pktDropper_Montreal_Toronto: pktDropper {
            @display("i=abstract/opticalswitch_vs;p=1642.815,100.619995");
        }
        pktDropper_Toronto_London: pktDropper {
            @display("i=abstract/opticalswitch_vs;p=1774.395,178.02");
        }
        pktDropper_Toronto_Oakville: pktDropper {
            @display("i=abstract/opticalswitch_vs;p=1838.25,79.335");
        }
        pktDropper_Chicago_Detroit: pktDropper {
            @display("i=abstract/opticalswitch_vs;p=1838.25,359.91");
        }
        pktDropper_Oakville_London: pktDropper {
            @display("i=abstract/opticalswitch_vs;p=1965.96,129.645");
        }
        pktDropper_Detroit_London: pktDropper {
            @display("i=abstract/opticalswitch_vs;p=1884.69,255.42");
        }


        sdnController: sdnController {
            @display("p=1617.66,296.055");
        }

        pktgen1: pktgen {
            @display("i=msg/mail;p=176.08499,34.829998");
        }
        Victoria: node {
            @display("i=abstract/switch;p=56.114998,94.814995");
        }
        Vancouver: node {
            @display("i=abstract/switch;p=406.35,181.89");
        }
        Edmonton: node {
            @display("i=abstract/switch;p=789.48,114.165");
        }
        Calgary: node {
            @display("i=abstract/switch;p=774,249.61499");
        }
        Saskatoon: node {
            @display("i=abstract/switch;p=938.475,121.905");
        }
        Regina: node {
            @display("i=abstract/switch;p=911.385,265.095");
        }
        Winnipeg: node {
            @display("i=abstract/switch;p=1102.95,218.655");
        }
        Thunderbay: node {
            @display("i=abstract/switch;p=1304.19,145.125");
        }
        Minneapolis: node {
            @display("i=abstract/switch;p=1356.4349,327.01498");
        }
        Sudbury: node {
            @display("i=abstract/switch;p=1457.0549,166.41");
        }
        Milwaukee: node {
            @display("i=abstract/switch;p=1503.495,394.74");
        }
        Toronto: node {
            @display("i=abstract/server;p=1621.53,166.41");
        }
        Ottawa: node {
            @display("i=abstract/switch;p=1348.695,48.375");
        }
        Montreal: node {
            @display("i=abstract/switch;p=1687.32,46.44");
        }
        Chicago: node {
            @display("i=abstract/switch;p=1704.735,412.155");
        }
        Oakville: node {
            @display("i=abstract/switch;p=1981.44,59.985");
        }
        Detroit: node {
            @display("i=abstract/switch;p=1904.0399,319.275");
        }
        Seattle: node {
            @display("i=abstract/switch;p=96.75,350.235");
        }
        London: node {
            @display("i=abstract/switch;p=1965.96,187.69499");
        }
    connections:
        Victoria.port++ <--> {  delay = 19s; } <--> pktDropper_Victoria_Vancouver.port++;
        pktDropper_Victoria_Vancouver.port++ <--> {  delay = 19s; } <--> Vancouver.port++;
        Victoria.port++ <--> {  delay = 29s; } <--> pktDropper_Victoria_Seattle.port++;
        pktDropper_Victoria_Seattle.port++ <--> {  delay = 29s; } <--> Seattle.port++;
        Vancouver.port++ <--> {  delay = 38s; } <--> pktDropper_Vancouver_Seattle.port++;
        pktDropper_Vancouver_Seattle.port++ <--> {  delay = 38s; } <--> Seattle.port++;
        Vancouver.port++ <--> {  delay = 193s; } <--> pktDropper_Vancouver_Edmonton.port++;
        pktDropper_Vancouver_Edmonton.port++ <--> {  delay = 193s; } <--> Edmonton.port++;
        Vancouver.port++ <--> {  delay = 162s; } <--> pktDropper_Vancouver_Calgary.port++;
        pktDropper_Vancouver_Calgary.port++ <--> {  delay = 162s; } <--> Calgary.port++;
        Edmonton.port++ <--> {  delay = 50s; } <--> pktDropper_Edmonton_Calgary.port++;
        pktDropper_Edmonton_Calgary.port++ <--> {  delay = 50s; } <--> Calgary.port++;
        Edmonton.port++ <--> {  delay = 87s; } <--> pktDropper_Edmonton_Saskatoon.port++;
        pktDropper_Edmonton_Saskatoon.port++ <--> {  delay = 87s; } <--> Saskatoon.port++;
        Calgary.port++ <--> {  delay = 126s; } <--> pktDropper_Calgary_Regina.port++;
        pktDropper_Calgary_Regina.port++ <--> {  delay = 126s; } <--> Regina.port++;
        Saskatoon.port++ <--> {  delay = 130s; } <--> pktDropper_Saskatoon_Winnipeg.port++;
        pktDropper_Saskatoon_Winnipeg.port++ <--> {  delay = 130s; } <--> Winnipeg.port++;
        Regina.port++ <--> {  delay = 95s; } <--> pktDropper_Regina_Winnipeg.port++;
        pktDropper_Regina_Winnipeg.port++ <--> {  delay = 95s; } <--> Winnipeg.port++;
        Winnipeg.port++ <--> {  delay = 117s; } <--> pktDropper_Winnipeg_Thunderbay.port++;
        pktDropper_Winnipeg_Thunderbay.port++ <--> {  delay = 117s; } <--> Thunderbay.port++;
        Winnipeg.port++ <--> {  delay = 92s; } <--> pktDropper_Winnipeg_Minneapolis.port++;
        pktDropper_Winnipeg_Minneapolis.port++ <--> {  delay = 92s; } <--> Minneapolis.port++;
        Thunderbay.port++ <--> {  delay = 168s; } <--> pktDropper_Thunderbay_Sudbury.port++;
        pktDropper_Thunderbay_Sudbury.port++ <--> {  delay = 168s; } <--> Sudbury.port++;
        Minneapolis.port++ <--> {  delay = 90s; } <--> pktDropper_Minneapolis_Milwaukee.port++;
        pktDropper_Minneapolis_Milwaukee.port++ <--> {  delay = 90s; } <--> Milwaukee.port++;
        Sudbury.port++ <--> {  delay = 69s; } <--> pktDropper_Sudbury_Toronto.port++;
        pktDropper_Sudbury_Toronto.port++ <--> {  delay = 69s; } <--> Toronto.port++;
        Milwaukee.port++ <--> {  delay = 25s; } <--> pktDropper_Milwaukee_Chicago.port++;
        pktDropper_Milwaukee_Chicago.port++ <--> {  delay = 25s; } <--> Chicago.port++;
        Toronto.port++ <--> {  delay = 75s; } <--> pktDropper_Toronto_Ottawa.port++;
        pktDropper_Toronto_Ottawa.port++ <--> {  delay = 75s; } <--> Ottawa.port++;
        Ottawa.port++ <--> {  delay = 33s; } <--> pktDropper_Ottawa_Montreal.port++;
        pktDropper_Ottawa_Montreal.port++ <--> {  delay = 33s; } <--> Montreal.port++;
        Montreal.port++ <--> {  delay = 90s; } <--> pktDropper_Montreal_Toronto.port++;
        pktDropper_Montreal_Toronto.port++ <--> {  delay = 90s; } <--> Toronto.port++;
        Toronto.port++ <--> {  delay = 32s; } <--> pktDropper_Toronto_London.port++;
        pktDropper_Toronto_London.port++ <--> {  delay = 32s; } <--> London.port++;
        Toronto.port++ <--> {  delay = 7s; } <--> pktDropper_Toronto_Oakville.port++;
        pktDropper_Toronto_Oakville.port++ <--> {  delay = 7s; } <--> Oakville.port++;
        Chicago.port++ <--> {  delay = 76s; } <--> pktDropper_Chicago_Detroit.port++;
        pktDropper_Chicago_Detroit.port++ <--> {  delay = 76s; } <--> Detroit.port++;
        Oakville.port++ <--> {  delay = 26s; } <--> pktDropper_Oakville_London.port++;
        pktDropper_Oakville_London.port++ <--> {  delay = 26s; } <--> London.port++;
        Detroit.port++ <--> {  delay = 34s; } <--> pktDropper_Detroit_London.port++;
        pktDropper_Detroit_London.port++ <--> {  delay = 34s; } <--> London.port++;



        Victoria.port++ <--> {  delay = 0s; } <--> pktgen1.port;
        sdnController.port++ <--> {  delay = 0s; } <--> Toronto.port++;
}

