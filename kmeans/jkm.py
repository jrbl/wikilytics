#!/usr/bin/python
# -*- coding: utf-8 -*-

"""jkm - a simple driver for k-means clustering using SciPy

Copyright (C) 2009  Joe Blaylock <jrbl@jrbl.org>

This program is free software: you can redistribute it and/or modify it under 
the terms of the GNU General Public License as published by the Free Software 
Foundation, either version 3 of the License, or (at your option) any later 
version.

This program is distributed in the hope that it will be useful, but WITHOUT 
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or 
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more 
details.

You should have received a copy of the GNU General Public License along with 
this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os, sys
sys.path.append(os.pardir + os.sep + 'pca')

import scipy.cluster.vq as vq
from JData import JData as Data 


DEBUG = False
CLUSTERS = 4
TRIALS = 1000


def count(l, v):
    """Count occurences of v in l"""
    return sum([1 for x in l if x == v])

def findall(l, v):
    """Yield all indices of v in l"""
    for i in range(len(l)):
        if l[i] == v:
            yield i

def do_cluster(cluster_count, filename):
    """Use the scipy k-means clustering algorithms to cluster data.

    Return the item names for the smallest cluster.
    """
    input = Data(filename, -1)
    d = vq.whiten(input.data.transpose())
    codebook, avg_distortion = vq.kmeans(d, cluster_count, 150)
    codes, distortions = vq.vq(d, codebook)

    # codes is now a vector of cluster assignments
    # it is ordered the same as data elements in input

    c_sizes = {}
    small_i = 0
    if DEBUG: print "Cluster Sizes: ",
    for i in range(cluster_count):
        c_sizes[i] = count(codes, i)
        if DEBUG: print c_sizes[i],
    if DEBUG: print
    for i in range(cluster_count):
        if c_sizes[i] < c_sizes[small_i]: 
            small_i = i

    if DEBUG: print "Smallest cluster size: " + str(c_sizes[small_i])

    return [input._names[i] for i in findall(codes, small_i)]


if __name__ == "__main__":

    files  = ['withRC.csv', 'noRC.csv']

    for FILE in files:
        small_members = {}

        for i in range(TRIALS):
            print "Run " + str(i) + ".. ",
            smallest = do_cluster(CLUSTERS, FILE)
            print "done." + str(len(smallest))
            sys.stdout.flush()

            for key in smallest:
                try:
                    small_members[key] += 1
                except KeyError:
                    small_members[key] = 1

        # who are the winners?
        keys = small_members.keys()
        vals = [small_members[key] for key in keys]
        indices = range(len(keys))

        def byVal_Comp(x, y):
            if vals[x] < vals[y]:
                return -1
            elif vals[x] > vals[y]:
                return 1
            else:
                return 0

        indices.sort(cmp=byVal_Comp, reverse=True)
        outfile = open(FILE+'.out', 'w')
        for i in indices:
            outfile.write(keys[i] + ',' + str(vals[i]) + '\n')
        outfile.close()
