import os
import time
import matplotlib.pyplot as plt
import sys

def graphic():
    f1 = open('ph1_p', 'r')
    ping1 = f1.readlines()
    f1.close()

    f2 = open('ph2_p', 'r')
    ping2 = f2.readlines()
    f2.close()

    f3 = open('ph3_p', 'r')
    ping3 = f3.readlines()
    f3.close()

    # initialize some variable to be lists:
    time_ = []
    
    l1 = []
    l2 = []
    l3 = []
    l4 = []
    
    # scan the rows of the file stored in lines, and put the values into some variables:
    i = 0
    for x in ping1:
        if x != '' and x != "\n":
            l1.append(float(x))

    for x in ping2:
        if x != '' and x != "\n":
            l2.append(float(x))

    for x in ping3:
        if x != '' and x != "\n":
            l3.append(float(x))
    
    l4 = l1 + l2 + l3

    i = 0
    for x in range(len(l4)):    
        time_.append(i)
        i = i + 1
    
    fig, ax1 = plt.subplots()
    
    ax1.plot(time_, l4, color='red', label='Latency', ls="--", markevery=7, linewidth=1)
    ax1.legend(loc=2, borderaxespad=0., fontsize=12)

    ax1.set_ylabel("Ping (msec)", fontsize=18)
    ax1.set_xlabel("Time (seconds)", fontsize=18)
    plt.savefig("graphicPING.eps")
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
