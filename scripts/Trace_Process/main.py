#!/usr/bin/env Python
# Total time for which application threads were stopped: 0.0008220 seconds
# Application time: 0.0275980 seconds

# Update 02/15/2014: 40 iterations, first 39 are warmup

import string
import sys
import os
import matplotlib.pyplot as plt

colors = ['0.1', '0.25', '0.4', '0.55', '0.7', '0.85', '1']



def helper(filename):
  fp = open(filename, 'r')
  ratiolist = []
  resultlist = []
  stoplist = []
  runlist = []
  res_stop = []
  res_run = []
  gctime_list = []
  gctime = 0.000
  gclist = []
  gc = 0
  flag = 0 # default flag: pass the warmup, calculate at the final run
  for line in fp:
    if line.find("starting ===") >= 0: # passed all 39 warmup
      flag = 1
      continue
    if flag == 1:
      if line.find("->") >= 0: # GC happens
        word = line.split("K->")
        word2 = line.split()
        gctime += float(word2[word2.index("secs]")-1])
        gc += 1
      elif line.find("threads were stopped:") >=0:  # the stopped time
        word = line.split(": ")
        stop = word[1].split(' ')[0]
        stoplist.append(float(stop))
      elif line.find("Application time: ") >=0:   # the running time
        word = line.split(": ")
        run = word[1].split(' ')[0]
        runlist.append(float(run))
      """
      elif line.find("%%%%%%%%%%") >=0:  # new session begins
        gctime_list.append(gctime)
        resultlist = []
        res_stop.append(float(sum(stoplist)))
        stoplist = []
        res_run.append(float(sum(runlist)))
        runlist = []
        gctime = 0.00
        gclist.append(gc)
        gc = 0
      """
#        flag = 0
  fp.close()
  return gctime, float(sum(runlist)), gc
  '''
  print filename
  print "\n\t Object Survive ratio is, ", float(float(sum(ratiolist))/float(len(ratiolist)))
  print "\t Application GC time total is, ", float(float(sum(gctime_list))/float(len(gctime_list)))
  print "\t Application stoppend time total is, ", float(float(sum(res_stop))/(float(len(res_stop))))
  print "\t Application run time total is, ", float(float(sum(res_run))/float(len(res_run)))
  '''
#  return (float(float(sum(gctime_list))/float(len(gctime_list))), float(float(sum(res_run))/float(len(res_run))), float(sum(gclist)/len(gclist)))

'''
def eachplot(name, inlist1, inlist2):
  """ plot each benchmark
  group by different gc threads, inlist1 is gclist, inlist2 is mutatorlist
  """
  xlist = ['1\nParallel: 1\nGC Thread', '2', '4','8', '16', '32', '48', ' ','1\n    2', '2', '4','8', '16', '32', '48', ' ', '1\n   4', '2', '4','8', '16', '32', '48', ' ', '1\n   8', '2', '4','8', '16', '32', '48']
  ylist1 = [] # gc fractions
  ylist2 = [] # mutator fractions
  for i in inlist1:
    for j in i:
      ylist1.append(j)
    ylist1.append(0.0)
  for i in inlist2:
    for j in i:
      ylist2.append(j)
    ylist2.append(0.0)
  plt.bar(range(len(ylist1)), ylist1, color="#000000", label="Pause Time")
  plt.bar(range(len(ylist2)), ylist2, bottom=ylist1, color='#d3d3d3', label="Completion time")
#  plt.xticks(range(len(xlist)), xlist)
  plt.title(name)
#  plt.legend(loc="upper center", ncol=2)
  plt.ylabel("Execution time (seconds)")
  plt.xlabel("Different processor cores")
  plt.savefig(name+"_different_GCThread.pdf", format='pdf', bbox_inches='tight')
  plt.cla()
'''

def plot(gcdict, mutatordict):
  namelist = []
  j = -1
  xlist = []
  ylist1 = []  # GC
  ylist2 = []  # mutator
  ylist11 = []
  ylist22 = []
#  namelist = ['lusearch', 'xalan', 'sunflow', 'h2', 'eclipse', 'jython', 'scalac', 'scaladoc', 'scalatest']
  for name in gcdict:
    j += 1
    xlist.append('   1\n          '+name)
    xlist.append('   2')
    xlist.append('   4')
    xlist.append('   6')
#    xlist.append('   8\n     "D"')
    xlist.append('    8')
#    xlist.append('   12')
    xlist.append('   16')
    xlist.append('   18\n   "D"')
    xlist.append('   24')
#    xlist.append('   32\n   "D"')
#    xlist.append('   48')
    xlist.append(' ')
    list1 = []
    list2 = []
    list11 = []
    list22 = []

#    eachplot(name, gcdict[name], mutatordict[name])

    list1 = gcdict[name]
    list2 = mutatordict[name]
    list11 = gcdict[name]
    list22 = mutatordict[name]
#    base = list1[0] + list2[0]
    base = list1[0]
    for i in range(len(list1)):
      list1[i] = float(list1[i])/float(base)
      list2[i] = float(list2[i])/float(base)
#      base2 = list11[i] + list22[i]
#      list11[i] = float(list11[i])/base2
#      list22[i] = float(list22[i])/base2
      ylist1.append(list1[i])
      ylist2.append(list2[i])
#      ylist11.append(list11[i])
#      ylist22.append(list22[i])
    ylist1.append(0.0)
    ylist2.append(0.0)
#    ylist11.append(0.0)
#    ylist22.append(0.0)
  del xlist[-1]
  del ylist1[-1]
  del ylist2[-1]
  plt.figure(figsize=(25, 10))
  plt.bar(range(len(ylist1)), ylist1, color="#000000", edgecolor='black')
#  plt.bar(range(len(ylist1)), ylist1, color="#000000", label="GC Time", edgecolor='black')
#  plt.bar(range(len(ylist2)), ylist2, bottom=ylist1, color='#d3d3d3', label="Application Run Time", edgecolor='black')
  plt.xticks(range(len(xlist)), xlist, fontsize = 10)
  plt.xlim([0, len(xlist)])
#  plt.legend(loc="upper center", ncol=2)
  plt.xlabel("Parallel GC thread number")
  plt.ylabel("Fraction of GC and mutator in total")
  plt.savefig("gcfraction.pdf", format='pdf', bbox_inches='tight')
  plt.cla()
'''
  plt.figure(figsize=(20, 10))
  plt.bar(range(len(ylist2)), ylist2, color="#d3d3d3", label="Completion Time")
  plt.bar(range(len(ylist1)), ylist1, bottom=ylist2, color='#000000', label="Pause Time")
  plt.grid()
  plt.xticks(range(len(xlist)), xlist)
  plt.xlim([0, len(xlist)])
  plt.legend(loc="upper center", ncol=2)
#  plt.gca()
  plt.xlabel("Benchmarks run with different processor cores number")
  plt.ylabel("Execution time normalized to single-thread execution")
  plt.savefig("mutator_GC_overall_performance.pdf", format='pdf', bbox_inches='tight')
  plt.cla()

  plt.figure(0, figsize=(20, 10))
  ylist = []
  for i in range(len(ylist1)):
    ylist.append(ylist1[i]+ylist2[i])
  plt.bar(range(len(ylist)), ylist, color="#d3d3d3")
  plt.xticks(range(len(xlist)), xlist)
  plt.xlim([0, len(xlist)])
  plt.grid()
  plt.xlabel("Benchmarks run with different processor cores number")
  plt.ylabel("Execution time normalized to single-thread execution")
  plt.savefig("overall_performance.pdf", format='pdf', bbox_inches='tight')
  plt.cla()
'''

markerlist = ['.', ',', 'o', 'v', '^', '*', '<', '>', 's', 'p', 'x', 'D']
def lineplot(gcfreqdict):
  namelist = []
  i = -1
  xlist = ['1', '2', '4', '8', '16', '32', '48']
  ylist = []
  for name in gcfreqdict:
    i += 1
    ylist = []
    namelist.append(name)
    base = gcfreqdict[name][0]
    for gc in gcfreqdict[name]:
      ylist.append(float(gc/base))
    plt.figure(0)
    plt.plot(range(len(ylist)), ylist, marker=markerlist[i], color='#d3d3d3',label=name)
    plt.savefig("GC_Frequency.pdf", format='pdf', bbox_inches='tight')
  plt.figure(0)
  plt.xticks(range(len(xlist)), xlist)
  plt.ylabel("Number of GC")
  plt.xlabel("Benchmarks run with different processor cores number")
  plt.legend(loc="upper left", ncol=3)
  plt.savefig("GC_Frequency.pdf", format='pdf', bbox_inches='tight')
  plt.cla()

def main():
  try:
    script, filename = sys.argv
  except:
    sys.exit("Usage: Filepath needed\n")
  gcdict = {}
  mutatordict = {}
  gcfreqdict = {}
#  thread = ['1', '2', '4', '8', '16', '32', '48']
#  thread = ['1', '2', '4', '6', '8']
  thread = ['1', '2', '4', '6', '8', '16', '18', '24']
#  gcthread = ['1', '2', '4', '8']
  if os.path.isfile(filename):
    print filename, helper(filename)
  else:
    for root, dirs, files in os.walk(filename):
      fnames = [os.path.join(root, f) for f in files]
      for f in fnames:
        (gctime, mutatortime, gcfrequency) = helper(f)
        name = (f.split('_')[-2]).split('/')[-1]
        threadid = f.split('_')[-1]
#        gcthreadid = f.split('_')[-1]
        index = thread.index(threadid)
#        gcindex = gcthread.index(gcthreadid)
        if not name in gcdict:
          gcdict[name] = []
          mutatordict[name] = []
          gcfreqdict[name] = []
          for ii in range(len(thread)):
            gcdict[name].append(0)
            mutatordict[name].append(0)
            gcfreqdict[name].append(0)
#          for gccount in range(4):
#            gcdict[name].append([0, 0, 0, 0, 0, 0, 0])
#            mutatordict[name].append([0, 0, 0, 0, 0, 0, 0])
        gcdict[name][index] = gctime
        mutatordict[name][index] = mutatortime
        gcfreqdict[name][index] = gcfrequency
  for name in gcdict:
	  print name
	  print gcdict[name]
  plot(gcdict, mutatordict)
#  lineplot(gcfreqdict)

if __name__ == "__main__":
  main()
