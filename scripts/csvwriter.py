#!/usr/bin/python

import string
import os
import sys
import csv
import datetime

now = datetime.datetime.now() 

def phase(filename):
  paralist = [0]
  init = 0
  begin = 0
  para = 0
  end = 0
  fina = 0
  for line in open(filename):
    word = line.split()
    if line.find("[GC") >= 0:
#      if (min(paralist) - begin) < 0 or max(paralist) - min(paralist)<0 or end - max(paralist) < 0:
#        print filename, min(paralist), begin, max(paralist), end
#        sys.exit(line)
      while (min(paralist) - begin) < 0:
        paralist.remove(min(paralist))
      init += min(paralist) - begin
      para += max(paralist) - min(paralist)
      fina += end - max(paralist)
      paralist = []
      begin = 0
      end = 0
    elif line.find("VM-Thread ") >= 0:
      begin = int(word[1])
      end = int(word[-1])
    elif line.find("-task") >= 0:
      paralist.append(int(word[-2]))
      paralist.append(int(word[-3]))
  init += min(paralist) - begin
  para += max(paralist) - min(paralist) 
  fina += end - max(paralist) 
  return str(init), str(para), str(fina)

if __name__ == "__main__":
  bms = ["pmd", "avrora", "h2", "jython", "sunflow", "xalan", "xml.transform", "xml.validation", "lusearch", "eclipse", "tomcat"]
  ret = csv.writer(open("time_%s_%s.csv"%(now.day, now.minute), "wb"))
  ts = ["1"]
#  for i in range(1, 48, 4):
#    ts.append(str(i))
  for bm in bms:
    ret.writerow([bm])
    for i in ts:
      filename = sys.argv[1] + os.sep + bm + "_" + i + "_default"
      default_init, default_para, default_fina = phase(filename)
      filename = sys.argv[1] + os.sep + bm + "_" + i + "_nostealing"
      nostealing_init, nostealing_para, nostealing_fina = phase(filename)
      filename = sys.argv[1] + os.sep + bm + "_" + i + "_smartstealing"
      smart_init, smart_para, smart_fina = phase(filename)
#      ret.writerow(["", i, default_para, default_init, default_fina, "", nostealing_para, nostealing_init, nostealing_fina, "", smart_para, smart_init, smart_fina])
      ret.writerow(["", i, default_para, default_init, default_fina])
#      ret.writerow(["", i, nostealing_para, nostealing_init, nostealing_fina])
#      ret.writerow(["", i, smart_para, smart_init,smart_fina])
      ret.writerow([])
