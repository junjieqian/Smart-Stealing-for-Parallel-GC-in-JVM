#!/usr/bin/python

import string
import os
import logreader
import taskreader
import csv
import datetime

def phasewrite(filepath):
    read = logreader.reader(filepath)
    read.read()
    phase = read.getphase()
    if not os.path.isdir("results"):
        os.mkdir("results")
    now = datetime.datetime.now() 
    ret = csv.writer(open("throughput_%s_%s.csv"%(now.day, now.minute), "wb"))
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
        ret.writerow(benchmark)
        for i in range(len(init_list)):
            if i%5 == 0 or i==47:
                xlist.append(str(i+1))
            else:
                xlist.append('')
            ret.writerow([" ", str(i), str(para_list[i]), str(init_list[i]), str(fina_list[i])])
#        print init_list, para_list, fina_list
