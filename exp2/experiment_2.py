# !/usr/bin/python

"""
Task 1: Implementation of the experiment described in the paper with title: 
"From Theory to Experimental Evaluation: Resource Management in Software-Defined Vehicular Networks"
http://ieeexplore.ieee.org/document/7859348/ 
"""

import os
import time
import matplotlib.pyplot as plt
from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch, OVSKernelAP
from mininet.link import TCLink
from mininet.log import setLogLevel, debug
from mininet.cli import CLI

import sys
gnet=None


# Implement the graphic function in order to demonstrate the network measurements
# Hint: You can save the measurement in an output file and then import it here
def graphic():
    f1 = open('./' + 'ifc_cl_rxp', 'r')
    cl_pkt = f1.readlines()
    f1.close()

    f11 = open('./' + 'ifc_cl_rxb', 'r')
    cl_throughput = f11.readlines()
    f11.close()

    f2 = open('./' + 'ifc_c0_txp', 'r')
    c0_pkt = f2.readlines()
    f2.close()

    f21 = open('./' + 'ifc_c0_txb', 'r')
    c0_throughput = f21.readlines()
    f21.close()

    # initialize some variable to be lists:
    time_ = []
    
    l1 = []
    l2 = []
    t1 = []
    t2 = []
        
    ll1 = []
    ll2 = []
    tt1 = []
    tt2 = []
    
    # scan the rows of the file stored in lines, and put the values into some variables:
    flag = False
    i = 0
    for x in cl_pkt:
        if "---" in x:
            flag = True
            continue
        p = x.split()
        l1.append(int(p[0]))
        if flag is True:
            flag = False
            i += 1
            continue
        if len(l1) > 1:
            ll1.append(l1[i] - l1[i - 1])
        i += 1
    
    flag = False
    i = 0
    for x in cl_throughput:
        if "---" in x:
            flag = True
            continue
        p = x.split()
        t1.append(int(p[0]))
        if flag is True:
            flag = False
            i += 1
            continue
        if len(t1) > 1:
            tt1.append(t1[i] - t1[i - 1])
        i += 1
    
    i = 0
    for x in c0_pkt:
        if "---" in x:
            flag = True
            continue
        p = x.split()
        l2.append(int(p[0]))
        if flag is True:
            flag = False
            i += 1
            continue
        if len(l2) > 1:
            ll2.append(l2[i] - l2[i - 1])
        i += 1
    
    i = 0
    for x in c0_throughput:
        if "---" in x:
            flag = True
            continue
        p = x.split()
        t2.append(int(p[0]))
        if flag is True:
            flag = False
            i += 1
            continue
        if len(t2) > 1:
            tt2.append(t2[i] - t2[i - 1])
        i += 1
    
    i = 0
    for x in range(len(ll1)):    
        time_.append(i)
        i = i + 0.5
    
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    
    ax1.plot(time_, ll1, color='red', label='Received Data (client)', markevery=7, linewidth=1)
    ax1.plot(time_, ll2, color='black', label='Transmited Data (server)', markevery=7, linewidth=1)
    ax2.plot(time_, tt1, color='red', label='Throughput (client)', ls="-.", markevery=7, linewidth=1)
    ax2.plot(time_, tt2, color='black', label='Throughput (server)', ls=':', markevery=7, linewidth=1)
    ax1.legend(loc=2, borderaxespad=0., fontsize=12)
    ax2.legend(loc=1, borderaxespad=0., fontsize=12)

    ax2.set_yscale('log')

    ax1.set_ylabel("#Packets/sec", fontsize=18)
    ax1.set_xlabel("Time (seconds)", fontsize=18)
    ax2.set_ylabel("Throughput (bytes/sec)", fontsize=18)

    plt.savefig("graphic.eps")
    plt.show()

def apply_experiment(car,client,switch):
    print "Applying first phase"

    os.system('rm ifc_c0_txp ifc_cl_rxp ifc_c0_txb ifc_cl_rxb graphic.eps')
    # controller flows
    os.system('ovs-ofctl mod-flows switch in_port=1,actions=output:4')
    os.system('ovs-ofctl mod-flows switch in_port=3,actions=output:4')
    os.system('ovs-ofctl mod-flows switch in_port=4,actions=output:1,3')
    os.system('ovs-ofctl mod-flows switch in_port=2,actions=drop')
    
    #####

    # routing 
    car[0].cmd('ip route add 200.0.10.2 via 200.0.10.100')
    #####

    #CLI(gnet)
    taskTime = 20
    timeout = time.time() + taskTime
    currentTime = time.time()
    i = 0
    # measuring throughput
    while True: # getting received/transmitted bytes/packets from client and server for 20s 
        if time.time() > timeout:
            break;
        if time.time() - currentTime >= i:
            car[0].cmd('ifconfig bond0 | grep \"TX packets\" | awk -F\':\' \'{print $2}\' >> %s' % 'ifc_c0_txp') 
            client.cmd('ifconfig client-eth0 | grep \"RX packets\" | awk -F\':\' \'{print $2}\' >> %s' % 'ifc_cl_rxp')
            car[0].cmd('ifconfig bond0 | grep \"bytes\" | awk -F\':\' \'{print $3}\' >> %s' % 'ifc_c0_txb')
            client.cmd('ifconfig client-eth0 | grep \"bytes\" | awk -F\':\' \'{print $2}\' >> %s' % 'ifc_cl_rxb')
            i += 0.5

    os.system('echo \'---\' >> ifc_c0_txp')
    os.system('echo \'---\' >> ifc_cl_rxp')
    os.system('echo \'---\' >> ifc_c0_txb')
    os.system('echo \'---\' >> ifc_cl_rxb')
    
    #####
    
    # measuring latency
    car[0].cmd('ping 200.0.10.2 -c 20 > ph1_p_tmp1')
    os.system('awk \'!/(DUP!)/\' ph1_p_tmp1 | awk -F \"time=\" \'{print $2}\' | tail -24 | head -20 | awk \'{print $1}\' > ph1_p')
    #####

    # measuring jitter and packet loss
    client.cmd('iperf -s -u -i 1 > ph1_ip_tmp1 &')
    pid = int (client.cmd('echo $!'))
    car[0].cmd('iperf -c 200.0.10.2 -u -i 1 -t 20')
    client.cmd('kill -9 ' + str(pid))
    os.system('awk \'/\/sec/\' ph1_ip_tmp1 | awk -F \"/sec \" \'{print $2}\' | head -20 > ph1_ip')
    ######

    print "Moving nodes"
    car[0].moveNodeTo('150,100,0')
    car[1].moveNodeTo('120,100,0')
    car[2].moveNodeTo('90,100,0')
    car[3].moveNodeTo('70,100,0')

    print "Applying second phase"

    # controller flows
    os.system('ovs-ofctl mod-flows switch in_port=2,actions=output:4')
    os.system('ovs-ofctl mod-flows switch in_port=3,actions=output:4')
    os.system('ovs-ofctl mod-flows switch in_port=4,actions=output:2,3')
    os.system('ovs-ofctl mod-flows switch in_port=1,actions=drop')
    ###
    #CLI(gnet)
    #####
    timeout = time.time() + taskTime
    currentTime = time.time()
    i = 0
    
    # measuring throughput
    while True: # getting received/transmitted bytes/packets from client and server for 20s 
        if time.time() > timeout:
            break;
        if time.time() - currentTime >= i:
            car[0].cmd('ifconfig bond0 | grep \"TX packets\" | awk -F\':\' \'{print $2}\' >> %s' % 'ifc_c0_txp') 
            client.cmd('ifconfig client-eth0 | grep \"RX packets\" | awk -F\':\' \'{print $2}\' >> %s' % 'ifc_cl_rxp')
            car[0].cmd('ifconfig bond0 | grep \"bytes\" | awk -F\':\' \'{print $3}\' >> %s' % 'ifc_c0_txb')
            client.cmd('ifconfig client-eth0 | grep \"bytes\" | awk -F\':\' \'{print $2}\' >> %s' % 'ifc_cl_rxb')
            i += 0.5

    os.system('echo \'---\' >> ifc_c0_txp')
    os.system('echo \'---\' >> ifc_cl_rxp')
    os.system('echo \'---\' >> ifc_c0_txb')
    os.system('echo \'---\' >> ifc_cl_rxb')
    #####
    
    # measuring latency
    car[0].cmd('ping 200.0.10.2 -c 20 > ph2_p_tmp1')
    os.system('awk \'!/(DUP!)/\' ph2_p_tmp1 | awk -F \"time=\" \'{print $2}\' | tail -24 | head -20 | awk \'{print $1}\' > ph2_p')
    #####

    # measuring jitter and packet loss
    client.cmd('iperf -s -u -i 1 > ph2_ip_tmp1 &')
    pid = int (client.cmd('echo $!'))
    car[0].cmd('iperf -c 200.0.10.2 -u -i 1 -t 20')
    client.cmd('kill -9 ' + str(pid))
    os.system('awk \'/\/sec/\' ph2_ip_tmp1 | awk -F \"/sec \" \'{print $2}\' | head -20 > ph2_ip')
    #####
    print "Moving nodes"
    car[0].moveNodeTo('190,100,0')
    car[1].moveNodeTo('150,100,0')
    car[2].moveNodeTo('120,100,0')
    car[3].moveNodeTo('90,100,0')

    #time.sleep(2)
    print "Applying third phase"

    # controller flows
    os.system('ovs-ofctl mod-flows switch in_port=2,actions=output:4')
    os.system('ovs-ofctl mod-flows switch in_port=4,actions=output:2')
    os.system('ovs-ofctl mod-flows switch in_port=3,actions=drop')
    os.system('ovs-ofctl mod-flows switch in_port=1,actions=drop')
    ####
    
    timeout = time.time() + taskTime
    currentTime = time.time()
    i = 0
    #CLI(gnet)
    while True: # getting received/transmitted bytes/packets from client and server for 20s 
        if time.time() > timeout:
            break;
        if time.time() - currentTime >= i:
            car[0].cmd('ifconfig bond0 | grep \"TX packets\" | awk -F\':\' \'{print $2}\' >> %s' % 'ifc_c0_txp') 
            client.cmd('ifconfig client-eth0 | grep \"RX packets\" | awk -F\':\' \'{print $2}\' >> %s' % 'ifc_cl_rxp')
            car[0].cmd('ifconfig bond0 | grep \"bytes\" | awk -F\':\' \'{print $3}\' >> %s' % 'ifc_c0_txb')
            client.cmd('ifconfig client-eth0 | grep \"bytes\" | awk -F\':\' \'{print $2}\' >> %s' % 'ifc_cl_rxb')
            i += 0.5
    #####
    
    # measuring latency
    car[0].cmd('ping 200.0.10.2 -c 20 > ph3_p_tmp1')
    os.system('awk \'!/(DUP!)/\' ph3_p_tmp1 | awk -F \"time=\" \'{print $2}\' | tail -24 | head -20 | awk \'{print $1}\' > ph3_p')
    #####

    # measuring jitter and packet loss
    client.cmd('iperf -s -u -i 1 > ph3_ip_tmp1 &')
    pid = int (client.cmd('echo $!'))
    car[0].cmd('iperf -c 200.0.10.2 -u -i 1 -t 20')
    client.cmd('kill -9 ' + str(pid))
    os.system('awk \'/\/sec/\' ph3_ip_tmp1 | awk -F \"/sec \" \'{print $2}\' | head -20 > ph3_ip')
    #####
    
    os.system('rm ph1_ip_t* ph1_p_t* ph2_p_t* ph2_ip_t* ph3_p_t* ph3_ip_t*')


def topology():
    "Create a network."
    net = Mininet(controller=Controller, link=TCLink, switch=OVSKernelSwitch, accessPoint=OVSKernelAP)
    global gnet
    gnet = net

    print "*** Creating nodes"
    car = []
    for x in range(0, 4):
        car.append(x)
    for x in range(0, 4):
        car[x] = net.addCar('car%s' % (x), wlans=2, ip='10.0.0.%s/8' % (x + 1), \
        mac='00:00:00:00:00:0%s' % x, mode='b')

    
    eNodeB1 = net.addAccessPoint('eNodeB1', ssid='eNodeB1', dpid='1000000000000000', mode='ac', channel='1', position='80,75,0', range=60)
    eNodeB2 = net.addAccessPoint('eNodeB2', ssid='eNodeB2', dpid='2000000000000000', mode='ac', channel='6', position='180,75,0', range=60)
    rsu1 = net.addAccessPoint('rsu1', ssid='rsu1', dpid='3000000000000000', mode='g', channel='11', position='140,120,0', range=40)
    c1 = net.addController('c1', controller=Controller)
    client = net.addHost ('client')
    switch = net.addSwitch ('switch', dpid='4000000000000000')

    net.plotNode(client, position='125,230,0')
    net.plotNode(switch, position='125,200,0')

    print "*** Configuring wifi nodes"
    net.configureWifiNodes()

    print "*** Creating links"
    net.addLink(eNodeB1, switch)
    net.addLink(eNodeB2, switch)
    net.addLink(rsu1, switch)
    net.addLink(switch, client)

    print "*** Starting network"
    net.build()
    c1.start()
    eNodeB1.start([c1])
    eNodeB2.start([c1])
    rsu1.start([c1])
    switch.start([c1])

    i = 1
    j = 2
    for c in car:
        c.cmd('ifconfig %s-wlan0 192.168.0.%s/24 up' % (c, i))
        c.cmd('ifconfig %s-wlan1 192.168.1.%s/24 up' % (c, i))
        i += 2
        j += 2

    print "\n"
    client.cmd('ifconfig client-eth0 200.0.10.2')

    car[0].cmd('modprobe bonding mode=3')
    car[0].cmd('ip link add bond0 type bond')
    car[0].cmd('ip link set bond0 address 02:01:02:03:04:08')
    car[0].cmd('ip link set car0-wlan0 down')
    car[0].cmd('ip link set car0-wlan0 address 00:00:00:00:00:15')
    car[0].cmd('ip link set car0-wlan0 master bond0')
    car[0].cmd('ip link set car0-wlan1 down')
    car[0].cmd('ip link set car0-wlan1 address 00:00:00:00:00:13')
    car[0].cmd('ip link set car0-wlan1 master bond0')
    car[0].cmd('ip addr add 200.0.10.100/24 dev bond0')
    car[0].cmd('ip link set bond0 up')

    """plot graph"""
    net.plotGraph(max_x=250, max_y=250)

    net.startGraph()
    # streaming video
    car[0].cmdPrint("vlc -vvv ./bunnyMob.mp4 --sout '#duplicate{dst=rtp{dst=200.0.10.2,port=5004,mux=ts},dst=display}' :sout-keep --meta-title 'car0' &")
    client.cmdPrint("vlc rtp://@200.0.10.2:5004 --meta-title 'client' &")
    

    car[0].moveNodeTo('110,100,0')
    car[1].moveNodeTo('80,100,0')
    car[2].moveNodeTo('65,100,0')
    car[3].moveNodeTo('50,100,0')
    car[0].cmd('ip route add 200.0.10.2 via 200.0.10.100')

    apply_experiment(car,client,switch)

    # Uncomment the line below to generate the graph that you implemented
    graphic()

    # kills all the xterms that have been opened
    #--------------------- os.system('pkill xterm')

    print "*** Running CLI"
    CLI(net)

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    try:
        topology()
    except:
        type = sys.exc_info()[0]
        error = sys.exc_info()[1]
        traceback = sys.exc_info()[2]
        print ("Type: %s" % type)
        print ("Error: %s" % error)
        print ("Traceback: %s" % traceback)
        if gnet != None:
            gnet.stop()
        else:
            print "No network was created..."
