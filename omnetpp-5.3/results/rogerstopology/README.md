This directory contains simulation results for **Amaru** performed on Rogers network topology taken from the paper *"Fast Control Channel Recovery for Resilient
In-band OpenFlow Networks"*.

In these experiments, a packet generator starts to generate packets at 30ms and the link failure is triggered at 70ms (for more details on simulation settings, please see the *rogers.ini* file in *simulations* directory). The results are given in the "\*.csv" and "\*.eps" files. For example, in the "Amaru_failure_recovery_\*" files, you can see the time when the first and last packet arrives from the *.eps files. The time of last packet at failed link is the time when the failure occurs (69.9ms) and similarly the time of first packet at recovery link is the restore time (73.2ms). You can explore the *-plotdata.csv files for more detail where the first column lists simulation time and the second column shows traffic in packets/ms at the instant.

Summary of failure recovery results for single and multiple link failure is as follows-

|Link Failure Type |Outage Start	| Outage End |	Outage Duration |
------------------|---------------|------------|------------------|
|Single 1	|84.9|	88.9	|4|
|Single 2	|83.1	|110.3	|27.2|
|Single 3	|78.1	|106.1	|28|
|Single 4	|71.1	|104	|32.9|
|Simultaneous 2	|83.1	|112.3	|29.2|
|Simultaneous 3	|78.1	|112.3	|34.2|
|Simultaneous 4	|71.1|	112.4	|41.3|

Specification of the links are given here. Details can be found in *rogers.ned* file in *simulations* directory.

|Link Name	|Delay (ms)	|Distance|	Ring Size|
|---------|---------|--------------|-----------|
|Link 1 (Victoria-Vancouver)	|0.38|	11|	3|
|Link 2 (Vancouver-Calgary)	|3.24	|10|	2|
|Link 3 (Regina-Winnipeg)	|1.9	|8	|5|
|Link 4 (Detroit-London)	|0.68	|2|	9|
