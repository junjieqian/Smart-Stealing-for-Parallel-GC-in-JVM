#!/usr/bin/python

import sys
import string
import os
import matplotlib.pyplot as plt

def plot(indict):
    xlist = ['1', '2', '4', '8', '16', '32', '48']
    colorlist = ['#a9a9a9', '#f5f5f5']
    hatchlist = ['\\', '/']
    for bm in indict:
        list1 = indict[bm]
        for i in reversed(range(48)):
            list3 = []
            list2 = []
            for j in range(len(list1)):
                list2.append(list1[j][i])
                if i == 0:
                    list3.append(0.0)
                else:
                    list3.append(sum(list1[j][0:i]))
            plt.figure(0)
            plt.bar(range(len(list2)), list2, bottom=list3, color=colorlist[i%2],hatch=hatchlist[i%2], edgecolor='black')
        plt.xticks(range(len(xlist)), xlist)
        plt.xlabel("Parallel GC thread number")
        plt.title(bm)
        plt.savefig(bm+'.pdf', foramt = "pdf", bbox_inches='tight')
        plt.cla()
pass

def read(filename):
    fp = open(filename)
    runflag = False
    gcflag = False
    outlist = []
    flag = False
    gc_ite = {}
    for i in range(48):
        outlist.append(0.0) # each element is the "index" threads share the time period
    for line in fp:
        if runflag:
            if flag:
                word = line.split()
                gc_ite[tid].append(int(word[-3]))
                gc_ite[tid].append(int(word[-2]))
                cnt -= 1
                if cnt == 0:
                    flag = False
                 #   gc_ite[tid].sort()
            if line.find("[GC") >= 0 or line.find("[Full GC") >= 0:
            # process all the timestamps during the GC period
                timelist = []
                templist = []
                if (len(gc_ite)) < 1:
                    continue

                for i in range(48):
                    templist.append(0.0) # same as outlist but temp
                for i in gc_ite:
                    for j in gc_ite[i]:
                        timelist.append(j)

                timelist = list(set(timelist)) # remove the duplicates
                timelist.sort()
                sharethread = 0
                sharetime = 0.0
                last = timelist[0]
                for i in range(len(timelist)):
                    sharetime = timelist[i] - last
#                    if sharetime == 0.0: # this the starting
#                        continue
                    for ii in gc_ite:
                        for jj in range(len(gc_ite[ii])):
                            if gc_ite[ii][jj] == timelist[i]:
                                if jj%2==0: # starting
                                    sharethread += 1
                                else:
                                    sharethread -= 1
                    if sharetime == 0 or sharethread == 0:
                        continue
                   # print sharethread
                    templist[sharethread - 1] += sharetime
                    last = timelist[i]
                
               # for i in range(len(gc_ite)):
                for i in range(48):
                    outlist[i] += templist[i]
                templist = []
                gcflag = True
                gc_ite = {}
            if line.find("GC-Thread") >= 0:
                flag = True
                cnt = int(line.split()[-1])
                tid = int(line.split()[-3])
                if not tid in gc_ite:
                    gc_ite[tid] = []
        if line.find("starting ====") >= 0:
            runflag = True
    fp.close()
    outlist.reverse()
    #print outlist
    return outlist

if __name__ == "__main__":
    if os.path.isfile(sys.argv[1]):
        timelist = read(sys.argv[1])
    else:
        for root, dirs, files in os.walk(sys.argv[1]):
            fs = [os.path.join(root, f) for f in files]
            benchmark_gctime = {}
            thds = ['1', '2', '4', '8', '16', '32', '48']
            for i in fs:
                word = i.split('_')
                bm = word[0].split('/')[-1]
                if not bm in benchmark_gctime:
                    benchmark_gctime[bm] = [[],[],[],[],[],[],[]]
            for filename in fs:
                word = filename.split('_')
                bm = word[0].split('/')[-1]
                index = thds.index(word[1])
                benchmark_gctime[bm][index] = read(filename)
        plot(benchmark_gctime)
