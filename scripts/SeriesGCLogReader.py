#!/usr/bin/python

# Junjie Qian, jqian@cse.unl.edu

import string
import sys
import os
import matplotlib.pyplot as plt
import csv
import datetime

def timeplot(indict, ylabel=None):
  """ function to plot the gc time lengths
  plot, gc size change, gc time proportion, gc efficiency
  """
  if not ylabel:
    ylabel = "gc performance"
    plt.figure(0)
    xlist = ['1', '2', '4', '8', '16', '32', '48']
    markers = ['*', '^', 'o', '<', 'v', 's', 'p', 'x', 'D']
    cnt = 0
  for i in indict:
    ylist = []
    temp = indict[i][0]
    for j in indict[i]:
      ylist.append(float(j/temp))
    plt.plot(range(len(ylist)), ylist, marker=markers[cnt], label=i)
    cnt += 1
  plt.xlabel("Parallel GC thread number")
  plt.ylabel(ylabel)
  plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
  plt.xticks(range(len(xlist)), xlist)
  plt.savefig(ylabel+".pdf", format="pdf", bbox_inches="tight")
  plt.cla()


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
  for line in fp:
    #TODO: now only minor GC works, so collect minor only
    if line.find("[GC") >= 0:
      word = line.split()
      gctime.append(float(word[word.index("secs]")-1]))
      gcsize.append(1000 * (int(word[word.index("secs]") - 2].split('K')[0]) - int(word[word.index("secs]") - 2].split('->')[1].split('K')[0])))
    elif line.find("Application time: ") >= 0:
      word = line.split()
      apptime.append(float(word[-2]))
  fp.close()
  return (gctime, apptime, gcsize)

def gcdistribution(indict):
  """ function to plot time distributions of threads
  """
  xlist = ['1','2','4','8','16','32','48']
  colorlist = ['#a9a9a9','#f5f5f5']
  hatchlist = ['\\', '/']
  for name in indict:
    maxlength = 48
    list3 = []
    list1 = []
    inlist = indict[name]
    for i in range(maxlength):
      list1.append([])
      list3.append([])
      for j in range(len(inlist)):
        if i<len(inlist[j]):
          list1[i].append(inlist[j][i])
        else:
          list1[i].append(0.0)
        if i==0:
          list3[i].append(0.0)
        else:
          list3[i].append(list3[i-1][j] + list1[i-1][j])
    plt.figure(0)
    i = 0
    for n in range(48):
      plt.bar(range(len(list1[n])), list1[n], bottom=list3[n], color=colorlist[i%2], hatch=hatchlist[i%2], edgecolor="black")
      i+=1
    plt.xlabel("Parallel GC thread number")
    plt.ylabel("Fractions of GC threads' execution time in total")
    plt.xticks(range(len(xlist)), xlist)
    plt.title(name)
    plt.savefig(name+".pdf", format="pdf", bbox_inches="tight")
    plt.cla()

def gcthread(filename):
  fp = open(filename)
  flag = False
  runflag = False
  timedict = {}
  for line in fp:
    if line.find("starting ====") >= 0:
      runflag = True
    if runflag:
      if flag:
        word= line.split()
        cumutime = int(word[-2]) - int(word[-3])
        cnt -= 1
        if cnt == 0:
          flag = False
        timedict[tid] += cumutime
      if line.find("GC-Thread") >= 0:
        cnt = int(line.split()[-1])
        tid = int(line.split()[-3])
        if not tid in timedict:
          timedict[tid] = 0
        cumutime = 0
        flag = True
  timelist = []
  for i in timedict:
    timelist.append(timedict[i])
  timelist.sort(reverse=True)
  return timelist

def dirhelp(filepath):
  bms = ["avrora", "eclipse", "jython", "h2", "lusearch", "pmd", "sunflow", "tomcat", "xalan", "xml.transform", "xml.validation"]
#  bms = ["compiler.compiler", "compiler.sunflow", "compress", "crypto.aes", "crypto.rsa", "crypto.signverify", "mpegaudio", \
#  "scimark.sparse.small", "scimark.fft.small", "scimark.lu.small", "xml.validation", "xml.transform"]
  threads = []
  for i in range(1, 128, 4):
    threads.append(str(i))
  now = datetime.datetime.now()
  ret_throughput = csv.writer(open("throughput_%s_%s.csv"%(now.day, now.minute), "wb"))
  ret_throughput.writerow(["througput ","threads", "default", "no stealing", "smart stealing", \
    " ", " ", " ", "default", "no stealing", "smart stealing"])
  ret_time = csv.writer(open("time_%s_%s.csv"%(now.day, now.minute), "wb"))
  ret_time.writerow(["time ","threads", "default", "no stealing", "smart stealing", \
    " ", " ", " ", "default", "no stealing", "smart stealing"])
  for bm in bms:
    ret_time.writerow([bm])
    ret_throughput.writerow([bm])
    for i in threads:
      default = filepath + os.sep + bm + "_" + i + "_default"
      gctime, apptime, gcsize = helper(default)
      default_throughput = float(sum(gcsize)/sum(gctime))
      default_time = sum(gctime)
      nostealing = filepath + os.sep + bm + "_" + i + "_nostealing"
      gctime, apptime, gcsize = helper(nostealing)
      nostealing_time = sum(gctime)
      nostealing_throughput = float(sum(gcsize)/sum(gctime))
      smartstealing = filepath + os.sep + bm + "_" + i + "_smartstealing"
      gctime, apptime, gcsize = helper(smartstealing)
      smartstealing_time = sum(gctime)
      smartstealing_throughput = float(sum(gcsize)/sum(gctime))
      ret_time.writerow([" ", i, str(default_time), str(nostealing_time), str(smartstealing_time), \
        " ", " ", " ", "1", str(float(nostealing_time/default_time)), str(float(smartstealing_time/default_time))])
      ret_throughput.writerow([" ", i, str(default_throughput), str(nostealing_throughput), str(smartstealing_throughput), \
        " ", " ", " ", "1", str(float(nostealing_throughput/default_throughput)), str(float(smartstealing_throughput/default_throughput))])

def main():
  ''' main function
  explore the relationship between gc-thread number and other performances
  '''
  if os.path.isfile(sys.argv[1]):
    timelist = gcthread(sys.argv[1])
    gctime, apptime, gcsize = helper(sys.argv[1])
    print sum(gctime)
  else:
    dirhelp(sys.argv[1])

if __name__ == "__main__":
  main()
