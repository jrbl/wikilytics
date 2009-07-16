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


CLUSTERS = 4


def count(l, v):
    """Count occurences of v in l"""
    return sum([1 for x in l if x == v])

def findall(l, v):
    """Yield all indices of v in l"""
    for i in range(len(l)):
        if l[i] == v:
            yield i


if __name__ == "__main__":
    input = Data('data.csv', -1)
    d = vq.whiten(input.data.transpose())
    codebook, avg_distortion = vq.kmeans(d, CLUSTERS, 150)
    codes, distortions = vq.vq(d, codebook)

    # codes is now a vector of cluster assignments
    # it is ordered the same as data elements in input

    c_sizes = {}
    small_i = 0
    for i in range(CLUSTERS):
        c_sizes[i] = count(codes, i)
    for i in range(CLUSTERS):
        if c_sizes[i] < c_sizes[small_i]: 
            small_i = i

    print "Smallest cluster size: " + str(c_sizes[small_i])

    for i in findall(codes, small_i):
        print "\t" + input._names[i] 
