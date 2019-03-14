# Mininet Experiments

## Mininet-Wifi
Mininet-WiFi is a fork of [Mininet](http://mininet.org/) which allows the using of both WiFi Stations and Access Points. It is an emulator for Software Defined Networking that makes simple to create topologies and run network scenarios. For more details see [here](https://github.com/intrig-unicamp/mininet-wifi).

## Experiments
4 cars, 2 eNodeBs, 1 RSU (Road Side Unit), ovs, controller, client (safety center)

### First Experiment

#### Phase 1
3-hop V2V communication between the cars (in-band controlling) & V2I connectivity between car3 and eNodeB1
![Exp1_Ph1](https://github.com/patschris/MininetExperiments/blob/master/photos/Exp1_Ph1.PNG)

#### Phase 2
V2I communication between car0 and RSU, eNodeB2
![Exp1_Ph2](https://github.com/patschris/MininetExperiments/blob/master/photos/Exp1_Ph2.PNG)

#### Phase 3
V2I communication between car0 eNodeB2
![Exp1_Ph3](https://github.com/patschris/MininetExperiments/blob/master/photos/Exp1_Ph3.PNG)

Presented on the article ["From Theory to Experimental Evaluation: Resource Management in Software-Defined Vehicular Networks"](https://www.researchgate.net/publication/313872461_From_Theory_to_Experimental_Evaluation_Resource_Management_in_Software-Defined_Vehicular_Networks)


### Second Experiment

![Exp2_Ph1](https://github.com/patschris/MininetExperiments/blob/master/photos/Exp2_Ph1.PNG)
------
![Exp2_Ph2](https://github.com/patschris/MininetExperiments/blob/master/photos/Exp2_Ph2.PNG)
------

Presented on the article ["Mininet-WiFi: A Platform for Hybrid Physical-Virtual Software-Defined Wireless Networking Research"](https://www.researchgate.net/publication/305782558_Mininet-WiFi_A_Platform_for_Hybrid_Physical-Virtual_Software-Defined_Wireless_Networking_Research)


## Bicasting

## Measurements

### Throughput
The rate of successful message delivery over a communication channel (bits per second - bps). Measured via `ifconfig` command.

### Packet loss
Packet fail to reach destination while travelling across a computer network. 
Packet loss is either caused by errors in data transmission, typically across wireless networks or network congestion.
Measured via `iperf` command.

### Latency
Any kind of delay that happens in data communication over a network (milliseconds - ms). Measured via `ping` command.

### Jitter
The variation in latency as measured in the variability over time of the end-to-end delay across a network. 
Packet jitter is expressed as an average of the deviation from the network mean delay. Measured via `iperf` command.


## Comparison/Notes


## Graphs
