#!/usr/bin/python

import string
import os
import sys

class reader():
    def __init__(self, filepath):
        self.filepath = filepath
        self.tasks = {}

    def read(self):
        for root, dirs, files in os.walk(self.filepath):
            for f in files:
                fp = open(os.path.join(root, f))
                benchmark = f
                flag = False
                steals = {}
                roots = {}
                cnt = 0 # count GC occurence
                if not benchmark in self.tasks:
                    self.tasks[benchmark] = {"steal":{}, "roots":{}}
                for line in fp:
                    if line.find("[GC ") >= 0:
                        cnt += 1
                    if cnt != 3:
                        continue
                    if line.find("GC-Thread") >= 0:
                        flag = True
                        entries = int(line.split()[-1])
                        gctid = int(line.split()[1]) + 1
                    elif flag == True and entries >= 0:
                        s = int(line.split()[-3])
                        e = int(line.split()[-2])
                        if line.find("steal-task") >= 0:
                            if not gctid in steals:
                                steals[gctid] = []
                            steals[gctid].append([s, e])
                        else:
                            if not gctid in roots:
                                roots[gctid] = []
                            roots[gctid].append([s, e])
                        entries -= 1
                        if entries == 0:
                            flag = False
                self.tasks[benchmark]["steal"] = steals
                self.tasks[benchmark]["roots"] = roots
                fp.close()

    def gettasks(self):
        return self.tasks
