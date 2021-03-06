import os
import time
import matplotlib.pyplot as plt
import sys
import re

def graphic():

    f1 = open('ph1_ip_c0-c3', 'r')
    jpl1 = f1.readlines()
    f1.close()

    f11 = open('ph1_ip_c3-cl', 'r')
    jpl2 = f11.readlines()
    f11.close()

    f2 = open('ph2_ip', 'r')
    jpl3 = f2.readlines()
    f2.close()

    f21 = open('ph3_ip', 'r')
    jpl4 = f21.readlines()
    f21.close()

    # initialize some variable to be lists:
    time_ = []
    
    j1 = []
    pl1 = []
    j2 = []
    pl2 = []
    j3 = []
    pl3 = []
    j4 = []
    pl4 = []

    j = []
    pl = []
    
    # scan the rows of the file stored in lines, and put the values into some variables:
    for x in jpl1:    
        p = x.split()
        j1.append(float(p[0]))
        r = re.findall(r"\d*\.\d+|\d+",p[len(p) - 1])
        if len(r) > 0:        
            pl1.append(float(r[0]))

    for x in jpl2:    
        p = x.split()
        j2.append(float(p[0]))
        r = re.findall(r"\d*\.\d+|\d+",p[len(p) - 1])
        if len(r) > 0:        
            pl2.append(float(r[0]))

    for x in jpl3:    
        p = x.split()
        j3.append(float(p[0]))
        r = re.findall(r"\d*\.\d+|\d+",p[len(p) - 1])
        if len(r) > 0:        
            pl3.append(float(r[0]))

    for x in jpl4:    
        p = x.split()
        j4.append(float(p[0]))
        r = re.findall(r"\d*\.\d+|\d+",p[len(p) - 1])
        if len(r) > 0:        
            pl4.append(float(r[0]))


    s1 = [sum(i) for i in zip(j1,j2)]
    s2 = [sum(i) for i in zip(pl1,pl2)]

    j = s1 + j3 + j4
    pl = s2 + pl3 + pl4
    i = 0
    for x in range(len(j)):    
        time_.append(i)
        i = i + 1
    
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(time_, j, color='red', label='Jitter (msec)', ls="--", markevery=7, linewidth=1)
    ax2.plot(time_, pl, color='black', label='Packet Loss (%)', ls="-.", markevery=7, linewidth=1)
    ax1.legend(loc=2, borderaxespad=0., fontsize=12)
    ax2.legend(loc=1, borderaxespad=0., fontsize=12)

    ax1.set_ylabel("Jitter (msec)", fontsize=18)
    ax1.set_xlabel("Time (seconds)", fontsize=18)
    ax2.set_ylabel("Packet Loss (%)", fontsize=18)

    
    plt.savefig("graphicJPL.eps")
    plt.show()

if __name__ == '__main__':
    try:
        graphic()
    except:
        type = sys.exc_info()[0]
        error = sys.exc_info()[1]
        traceback = sys.exc_info()[2]
        print ("Type: %s" % type)
        print ("Error: %s" % error)
        print ("Traceback: %s" % traceback)
    sys.exit()
