#!/usr/bin/python

import string
import os
import sys

class reader():
    def __init__(self, filepath):
        self.filepath = filepath
        self.minor = {}
        self.major = {}
        self.gc = {}
        self.mutator = {}
        self.gcbalance = {}
        self.phases = {}

    def read(self):
        if not os.path.isfile(self.filepath):
            for roots, dirs, files in os.walk(self.filepath):
                fs = [os.path.join(roots, f) for f in files]
                for f in fs:
                    fp = open(f)
                    benchmark = (f.split('_')[-3]).split('/')[-1]
                    tid = int(f.split('_')[-2])-1
                    if not benchmark in self.minor:
                        self.minor[benchmark] = [0, 0, 0, 0, 0, 0, 0, 0]
                        self.major[benchmark] = [0, 0, 0, 0, 0, 0, 0, 0]
                        self.gc[benchmark] = [0, 0, 0, 0, 0, 0, 0, 0]
                        self.mutator[benchmark] = [0, 0, 0, 0, 0, 0, 0, 0]
                        self.gcbalance[benchmark] = [[], [], [], [], [], [], [], []]
                        self.phases[benchmark] = [[], [], [], [], [], [], [], []]
                    if tid >= 8 and len(self.minor[benchmark])<=tid:
                        for i in range(8, tid+1):
                            self.minor[benchmark].append(0)
                            self.major[benchmark].append(0)
                            self.gc[benchmark].append(0)
                            self.mutator[benchmark].append(0)
                            self.gcbalance[benchmark].append(0)
                            self.phases[benchmark].append([])
                    majorfreq = 0
                    majortime = 0
                    minorfreq = 0
                    minortime = 0
                    gcfreq = 0
                    gctime = 0
                    mutatortime = 0
                    flag = False
                    gcflag = False
                    entries = 0
                    gctid = -1
                    imbalance = []
                    gcthreadid = -1
                    initial_phase = 0
                    parallel_phase = 0
                    final_phase = 0
                    gcstarttime = 0
                    gcendtime = 0
                    gcpar_starttime = 0
                    gcpar_endtime = 0
                    for i in range(tid+1):
                        imbalance.append([])
                    for line in fp:
                        if line.find("[Full GC") >= 0:
                            majorfreq += 1
                            majortime += float(line.split()[-7])
                            gcfreq += 1
                            gctime += float(line.split()[-7])
                            gcflag = True
                        elif line.find("[GC") >= 0:
                            minorfreq += 1
                            minortime += float(line.split()[-7])
                            gcfreq += 1
                            gctime += float(line.split()[-7])
                            gcflag = True
                        elif line.find("Application time:") >= 0:
                            #initial_phase += gcpar_starttime - gcstarttime
                            #parallel_phase += gcpar_endtime - gcpar_starttime
                            #final_phase += gcendtime - gcpar_endtime
                            mutatortime += float(line.split()[-2])
                            gcflag = False
                            gcstarttime = 0
                            gcpar_starttime = 0
                            gcpar_endtime = 0
                            gcendtime = 0
                        elif line.find("VM-Thread") >= 0:
                            gcstarttime = int(line.split()[-3])
                            gcendtime = int(line.split()[-1])
                            #set the gc parallel phase start and end time in reverse
                            gcpar_starttime = gcendtime
                            gcpar_endtime = gcstarttime
                        elif line.find("GC-Thread") >= 0: ## find the distribution
                            flag = True
                            gcthreadid = int(line.split()[1]) - 1
                            entries = int(line.split()[-1])
                            temptime = 0
                        elif flag == True and line.find("-task") > 0:
                            if entries == 1:
                                flag = False
                                entries = 0
                                temptime += int(line.split()[-2]) - int(line.split()[-3])
                                imbalance.append(temptime)
                                temptime = 0
                                if int(line.split()[-2]) > gcpar_endtime:
                                    gcpar_endtime = int(line.split()[-2])
                                if int(line.split()[-3]) < gcpar_starttime:
                                    gcpar_starttime = int(line.split()[-3])
                                initial_phase += gcpar_starttime - gcstarttime
                                if gcpar_endtime - gcpar_starttime < 0:
                                    print line, f
                                    print gcpar_starttime, gcpar_endtime
                                    sys.exit()
                                parallel_phase += gcpar_endtime - gcpar_starttime
                                final_phase += gcendtime - gcpar_endtime
                            else:
                                entries -= 1
                                temptime += int(line.split()[-2]) - int(line.split()[-3])
                                if int(line.split()[-2]) > gcpar_endtime:
                                    gcpar_endtime = int(line.split()[-2])
                                if int(line.split()[-3]) < gcpar_starttime:
                                    gcpar_starttime = int(line.split()[-3])
                    self.minor[benchmark][tid] = minortime
                    self.major[benchmark][tid] = majortime
                    self.gc[benchmark][tid] = gctime
                    self.mutator[benchmark][tid] = mutatortime

                    self.phases[benchmark][tid].append(initial_phase)
                    self.phases[benchmark][tid].append(parallel_phase)
                    self.phases[benchmark][tid].append(final_phase)
                    print f, parallel_phase+initial_phase+final_phase, gctime
                    initial_phase = 0
                    parallel_phase = 0
                    final_phase = 0
                    fp.close()

    def getphase(self):
        return self.phases

    def getminor(self):
        # return the minor gcs and time
        return self.minor

    def getmajor(self):
        return self.major

    def getgc(self):
        return self.gc

    def getmutator(self):
        return self.mutator

    def getgcbalance(self):
        return self.gcbalance
