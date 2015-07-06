#!/usr/bin/python

# Junjie Qian, jqian@cse.unl.edu

import string
import sys
import os
import matplotlib.pyplot as plt

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
#		ylist = indict[i]
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
	runflag = True
	for line in fp:
		# if find the [GC [PSYoungGen: 18432K->3058K(21504K)]
		if line.find("starting ====") >= 0:
			runflag = True
		if runflag:
		#	if line.find("[GC") >= 0 or line.find("[Full GC") >= 0:
                        if line.find("secs]") >= 0:
				word = line.split()
	#			print word
				gctime.append(float(word[word.index("secs]")-1]))
        #                        print float(word[word.index("secs]")-1])
				# the GC efficiency
	#			before = int(word[word.index("[PSYoungGen:")+1].split('K')[0]) * 1024
	#			after = int(word[word.index("[PSYoungGen:")+1].split('->')[1].split('K')[0]) * 1024
	#			if word[word.index("[PSYoungGen:")+2].find('->') >= 0:
	#				before = int(word[word.index("[PSYoungGen:")+2].split('K')[0]) * 1024
	#				after = int(word[word.index("[PSYoungGen:")+2].split('->')[1].split('K')[0]) * 1024
	#			gcsize.append(-float(after - before)/float(before))
	#			print after-before
		#### TODO
			elif line.find("Application time: ") >= 0:
				word = line.split()
				apptime.append(float(word[-2]))
	fp.close()
#	print (gctime)
	return (gctime, apptime, gcsize)

def gcdistribution(indict):
    """ function to plot time distributions of threads
    """
    xlist = ['1','2','4','8','16','32','48']
    colorlist = ['#a9a9a9','#f5f5f5']
    hatchlist = ['\\', '/']
    for name in indict:
        maxlength = 48
        print name
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
        print list1[47]
#        for n in range(len(indict[name])):
#            plt.bar(range(len(list1[n])), list1[n], bottom=list3[n], color=colorlist[i%2], hatch=hatchlist[i%2], edgecolor='black')
#            i += 1
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
		#print cumutime
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

def main():
	''' main function
	explore the relationship between gc-thread number and other performances
	'''
	if os.path.isfile(sys.argv[1]):
		timelist = gcthread(sys.argv[1])
		#print timelist
		gctime, apptime, gcsize = helper(sys.argv[1])
		print sum(gctime)
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
					benchmark_gctotaltime[bm] = [0,0,0,0,0,0,0]
					benchmark_gcefficiency[bm] = [0,0,0,0,0,0,0]
					benchmark_apptotaltime[bm] = [0,0,0,0,0,0,0]
					benchmark_differentgctime[bm] = [[],[],[],[],[],[],[]]
			for filename in fs:
#				print filename
				word = filename.split('_')
				bm = word[0].split('/')[-1]
				index = thds.index(word[1])
				gctimetemp, apptimetemp, gcsizetemp = helper(filename)
				timelist = gcthread(filename)
				benchmark_gctotaltime[bm][index] = sum(gctimetemp)
				benchmark_gcefficiency[bm][index] = float(sum(gcsizetemp)/len(gcsizetemp))
				benchmark_apptotaltime[bm][index] = sum(apptimetemp)
				benchmark_differentgctime[bm][index] = timelist
			timeplot(benchmark_gctotaltime, "gctime")
			timeplot(benchmark_gcefficiency, "gcefficiency")
                #        gcdistribution(benchmark_differentgctime)

if __name__ == "__main__":
	main()
