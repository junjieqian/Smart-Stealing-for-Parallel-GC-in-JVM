#!/usr/bin/python

import string

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import logreader
import os

def box(filepath):
    reader = logreader.reader(filepath)
    reader.read()
    gc = reader.getbalance()
    if not os.path.isdir("results"):
        os.mkdir("results")
    for benchmark in gc:
        plt.figure(0)
        list1 = gc[benchmark]
