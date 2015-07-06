#!/usr/bin/python

import string
import os

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import logreader
import taskreader

markerlist = ['o', '^', '*', 'D', '+', 's', 'p', '>', '<', '1', 'h', 'x', '2', '3', '4', 'd', '|']


def gcplot(filepath, option):
    read = logreader.reader(filepath)
    read.read()
    if option == "minor":
        gc = read.getminor()
    elif option == "major":
        gc = read.getmajor()
    elif option == "gc":
        gc = read.getgc()
    elif option == "mutator":
        gc = read.getmutator()
    plt.figure(0)
    j = 0
    if not os.path.isdir("results"):
        os.mkdir("results")
    for benchmark in gc:
        xlist = []
        list1 = gc[benchmark]
        base = list1[0]
        for i in range(len(list1)):
            list1[i] = list1[i]/base
            if i == len(list1)-1:
                xlist.append(str(i+1))
            elif i%5 == 0:
                xlist.append(str(i+1))
            else:
                xlist.append('')
        plt.plot(range(len(xlist)), list1, marker=markerlist[j], label=benchmark)
        plt.xlabel("Parallel GC thread number")
        plt.ylabel("%s GC time"%option)
        plt.legend(loc="center left", bbox_to_anchor=(1,0.5))
        plt.savefig("results/%s_gc.pdf"%option, format="pdf", bbox_inches="tight")
        j += 1
    plt.cla()

def plotboth(filepath):
    read = logreader.reader(filepath)
    read.read()
    gc = read.getgc()
    mu = read.getmutator()
    if not os.path.isdir("results"):
        os.mkdir("results")
    plt.figure(0)
    for benchmark in gc:
#        plt.figure(0)
        list1 = gc[benchmark]
        list2 = mu[benchmark]
        xlist = []
        base1 = list1[0]
        base2 = list2[0]
        for i in range(len(list1)):
            if i == len(list1)-1:
                xlist.append(str(len(list1)))
            elif i%5 == 0:
                xlist.append(str(i+1))
            else:
                xlist.append('')
            list1[i] = list1[i]/list2[i]
#            list2[i] = list2[i]/base2
        plt.plot(xlist, list1, label=benchmark)
#        plt.plot(xlist, list2, label="Mutator")
    plt.xlabel("Parallel GC thread number")
    plt.ylabel("Normilization of GC/Mutator time")
    plt.legend(loc="upper center", ncol=6, fontsize=6)
    plt.savefig("results/bothtrend.pdf", format="pdf", bbox_inches="tight")
#        plt.cla()

def fraction(filepath):
    read = logreader.reader(filepath)
    read.read()
    gc = read.getgc()
    mu = read.getmutator()
    j = 0
    if not os.path.isdir("results"):
        os.mkdir("results")
    for benchmark in gc:
        plt.figure(0)
        list1 = gc[benchmark]
        list2 = mu[benchmark]
        xlist = []
        for i in range(len(list1)):
            if i==len(list1)-1:
                xlist.append(str(i+1))
            elif i%5 == 0:
                xlist.append(str(i+1))
            else:
                xlist.append('')
        #plt.figure(figsize=(20,10))
        plt.bar(range(len(xlist)), list2, color="#d3d3d3", label="Mutator time")
        plt.bar(range(len(xlist)), list1, bottom=list2, color="#000000", label="GC time")
        plt.xticks(range(len(xlist)), xlist)
        plt.legend(loc="center left", bbox_to_anchor=(1,0.5))
        plt.xlabel("Parallel GC thread number")
        plt.ylabel("Execution time")
        plt.savefig("results/%s_fraction.pdf"%benchmark, format="pdf", bbox_inches="tight")
        plt.cla()

def phaseplot2(filepath):
    read = logreader.reader(filepath)
    read.read()
    phase = read.getphase()
    if not os.path.isdir("results"):
        os.mkdir("results")

    for benchmark in phase:
        init_list = []
        para_list = []
        fina_list = []
        print benchmark
        for l in phase[benchmark]:
            try:
                init_list.append(l[0])
                para_list.append(l[1])
                fina_list.append(l[2])
            except:
                continue
        xlist = []
        for i in range(len(init_list)):
            if i%5 == 0 or i==47:
                xlist.append(str(i+1))
            else:
                xlist.append('')
        print init_list, para_list, fina_list
        plt.bar(range(len(xlist)), init_list, color="#d3d3d3", label="Initial phase")
        plt.bar(range(len(xlist)), para_list, bottom=init_list, color="#8b8878", label="Parallel phase")
        plt.bar(range(len(xlist)), fina_list, bottom=[para_list[j]+init_list[j] for j in range(len(para_list))], color="#000000", label="Final phase")
        plt.xticks(range(len(xlist)), xlist)
        plt.legend(loc="upper center", bbox_to_anchor=(0.5, 1.), ncol=3, prop={'size':10})
        plt.xlabel("Number of parallel GC threads")
        plt.ylabel("GC time distribution")
        plt.savefig("results/%s.pdf"%benchmark, format="pdf", bbox_inches="tight")
        plt.cla()

def phaseplot(filepath):
    read = logreader.reader(filepath)
    read.read()
    phases = read.getphase()
    if not os.path.isdir("results"):
        os.mkdir("results")
    xlist = ['1', '2', '4', '8', '16', '32']
    threads = []
    for i in range(100):
        threads.append(str(i*2+1))
    cnt = 0
    for i in range(3):
        cnt = 0
        ylist = []
        for j in range(len(phases["singlelinkedlist"])):
            ylist = []
            for benchmark in ["singlelinkedlist", "doublelinkedlist", "quadlinkedlist", "eightlinkedlist", "sixteenlinkedlist", "thirtytwolinkedlist"]:
                try:
                    ylist.append(phases[benchmark][j][i]/1000000000.0)
                except:
                    pass
            if len(ylist) == 0:
                continue
            if cnt%6 == 1:
                plt.figure(0)
                plt.plot(range(len(xlist)), ylist, label=threads[cnt])
            cnt+=1
        plt.figure(0)
        plt.xticks(range(len(xlist)), xlist)
        plt.xlabel("Number of linked lists")
        plt.ylabel("Time (secs)")
        plt.title(["Initial phase", "Parallel phase", "Final phase"][i])
        plt.legend(loc="center", bbox_to_anchor=(1, 0.5), title="number of\nGC threads")
        plt.rc('legend', **{'fontsize':6})
        plt.savefig(["initial", "parallel", "final"][i]+".pdf", format="pdf", bbox_inches="tight")
        plt.cla()

def gcthread(filepath):
    read = taskreader.reader(filepath)
    read.read()
    tasks = read.gettasks()
    minimums = []
    if not os.path.isdir("results"):
        os.mkdir("results")
    for benchmark in tasks:
        plt.figure(0)
        steals = tasks[benchmark]["steal"]
        roots = tasks[benchmark]["roots"]
        for gctid in steals:
            for ylist in steals[gctid]:
                plt.plot(ylist, [gctid, gctid], 'r+-')
                minimums.append(ylist[0])
                minimums.append(ylist[1])
        for gctid in roots:
            for ylist in roots[gctid]:
                plt.plot(ylist, [gctid, gctid], 'k*-')
                minimums.append(ylist[0])
                minimums.append(ylist[1])
        plt.xlim(min(minimums), max(minimums))
        minimums = []
        plt.ylim(0, 9)
        plt.xlabel("Ticks")
        plt.ylabel("GC thread index")
#        plt.legend(loc="center", bbox_to_anchor=(1, 0.5))
        plt.savefig("results/"+benchmark+".pdf", format="pdf", bbox_inches="tight")
        plt.cla()
