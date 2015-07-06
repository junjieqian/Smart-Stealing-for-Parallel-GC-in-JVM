#!/usr/bin/python

import string
import sys
from src import gcplot
from src import csvwriter

def main():
    usage = "Usage: %s <files> <options>: \n\tminor: minor GC frequency and time\n\tmajor: major GC frequency and time\n\tbox: boxplot the equalness of GC threads during each GC\n\tgcfraction: fraction of GC in total execution\n\tphase: print out the phases time fraction\n\tgcthreads: print out the execution time distribution of GC threads\n\tothers: todo "%sys.argv[0]
    if len(sys.argv) < 3:
        sys.exit(usage)
    filepath = sys.argv[1]
    option = sys.argv[2]
    if option == "minor":
        gcplot.gcplot(filepath, "gc")
    elif option == "major":
        gcplot.gcplot(filepath)
    elif option == "box":
        boxplot.boxplot(filepath)
    elif option == "gcfraction":
        gcplot.fraction(filepath)
    elif option == "trend":
        gcplot.plotboth(filepath)
    elif option == "phase":
        gcplot.phaseplot(filepath)
    elif option == "gcthreads":
        gcplot.gcthread(filepath)
    elif option == "phasecsv":
        csvwriter.phasewrite(filepath)
    else:
        print usage

if __name__ == "__main__":
    main()
