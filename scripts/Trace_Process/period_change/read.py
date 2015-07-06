#!/usr/bin/python

# Junjie Qian, jqian@cse.unl.edu

import string
import sys
import os
import matplotlib.pyplot as plt

def helper(filename):
    ''' helper function, sample the data
    To collect, 1. gc_threads entries ?
    2. gc time V.S. application time, throughput(average, highest, lowest)
    3. gc efficiency (average, highest, lowest)
    4. 
    '''
    fp = open(filename)
    gctime  = []   # time spent on GC, list
    apptime = []   # time spent on app, list
    gcsize  = []   # size collected by GC/size before collected, list
    runflag = False
    cum_app = 0
    for line in fp:
        # if find the [GC [PSYoungGen: 18432K->3058K(21504K)]
        if line.find("starting ====") >= 0:
            runflag = True
        if runflag:
            if line.find("[GC") >= 0 or line.find("[Full GC") >= 0:
                word = line.split()

                # the GC time proportion
                gctime.append(float(word[word.index("secs]")-1]))
                if cum_app > 0:
                    apptime.append(cum_app)
                cum_app = 0

                # the GC efficiency
                before = int(word[word.index("[PSYoungGen:")+1].split('K')[0]) * 1024
                after = int(word[word.index("[PSYoungGen:")+1].split('->')[1].split('K')[0]) * 1024
                if word[word.index("[PSYoungGen:")+2].find('->') >= 0:
                    before = int(word[word.index("[PSYoungGen:")+2].split('K')[0]) * 1024
                    after = int(word[word.index("[PSYoungGen:")+2].split('->')[1].split('K')[0]) * 1024
                gcsize.append(float(before - after)/float(before))
            elif line.find("Application time: ") >= 0:
                word = line.split()
                cum_app += float(word[-2])
    apptime.append(cum_app)
    fp.close()
    #print sum(gctime), sum(apptime)
    return (gctime, apptime, gcsize)

markers = ['o', '*', '^', 'D', 'p', 's', '<']
labels = ['1-thread', '2-thread', '4-thread', '8-thread', '16-thread', '32-thread', '48-thread']
def timeplot2(indict1, indict2):
    for bm in indict1:
        list1 = indict1[bm]
        list2 = indict2[bm]
        ylist = []
        for i in range(len(list1)):
            ylist.append([])
            if len(list1[i]) != len(list2[i]):
                print len(list1[i]), len(list2[i])
            for j in range(len(list1[i])):
                ylist[i].append(float(list1[i][j])/float(list2[i][j]))
        plt.figure(0)
        for i in range(len(ylist)):
            plt.plot(range(len(ylist[i])), ylist[i], marker=markers[i], label = labels[i])
        plt.xlabel("GC stamps during the execution")
        plt.ylabel("Proportion of GC time compared with app run time")
        plt.title(bm)
        plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        plt.savefig(bm+"_gctimepert.pdf", format="pdf", bbox_inches="tight")
        plt.cla()

def timeplot3(indict):
    for bm in indict:
        ylist = indict[bm]
        plt.figure(0)
        for i in range(len(ylist)):
            plt.plot(range(len(ylist[i])), ylist[i], marker=markers[i], label=labels[i])
        plt.xlabel("GC stamps during the execution")
        plt.ylabel("GC collection efficiency")
        plt.title(bm)
        plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        plt.savefig(bm+"_gceffi.pdf", format="pdf", bbox_inches="tight")
        plt.cla()

def main():
    ''' main function
    explore the relationship between gc-thread number and other performances
    '''
    if os.path.isfile(sys.argv[1]):
        timelist = gcthread(sys.argv[1])
        print timelist
        gctime, apptime, gcsize = helper(sys.argv[1])
        #print gctime
        #print apptime
        #print gcsize
    else:
        for root, dirs, files in os.walk(sys.argv[1]):
            fs = [os.path.join(root, f) for f in files]
            benchmark_gctotaltime = {} # key is the benchmark, value is the list of the values
            benchmark_apptotaltime = {}
            benchmark_gcefficiency = {}
            benchmark_differentgctime = {}
            thds = ['1', '2', '4', '8', '16', '32', '48']
            for i in fs:
                word = i.split('_')
                bm = word[0].split('/')[-1]
                if not bm in benchmark_gctotaltime:
                    benchmark_gctotaltime[bm] = [[],[],[],[],[],[],[]]
                    benchmark_gcefficiency[bm] = [[],[],[],[],[],[],[]]
                    benchmark_apptotaltime[bm] = [[],[],[],[],[],[],[]]
                    benchmark_differentgctime[bm] = [[],[],[],[],[],[],[]]
            for filename in fs:
#                print filename
                word = filename.split('_')
                bm = word[0].split('/')[-1]
                index = thds.index(word[1])
                gctimetemp, apptimetemp, gcsizetemp = helper(filename)
            #    timelist = gcthread(filename)
                benchmark_gctotaltime[bm][index] = gctimetemp
                benchmark_gcefficiency[bm][index] = gcsizetemp
                benchmark_apptotaltime[bm][index] = apptimetemp
            #    benchmark_differentgctime[bm][index] = timelist
    #        timeplot2(benchmark_gctotaltime, benchmark_apptotaltime)
            timeplot3(benchmark_gcefficiency)

if __name__ == "__main__":
    main()
