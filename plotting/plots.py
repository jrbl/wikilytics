#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########+#########+#########+#########+#########+#########+#########+#########+#########+#########+#########+#########+

"""Make it more convenient to do some data plotting

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


# Imports
import numpy
import matplotlib.pyplot as plt
from JData import JData as Data


# Classes


# Utility Functions
def get_bounded(xs, ys, xlower, xupper, ylower, yupper):
    new_xs = []
    new_ys = []
    for i in range(len(xs)):
        if (xs[i] >= xlower) and (xs[i] < xupper) and (ys[i] >= ylower) and (ys[i] < yupper):
            new_xs.append(xs[i])
            new_ys.append(ys[i])
    return new_xs, new_ys


# Test Harness
if __name__ == "__main__":

    X = 1
    Y = 2

    # read in data
    jd = Data('orig.csv')
    data = jd.data
    xs = jd.data[X]
    ys = jd.data[Y]

    xsig = jd.sigmas[X]
    ysig = jd.sigmas[Y]

    xcutoff = 2*xsig + xs.mean()
    ycutoff = 2*ysig + ys.mean()

    print "Xs:",jd._headings[2],"min", xs.min(), "max", xs.max(), "µ", xs.mean(), "s", xsig
    print "Ys:",jd._headings[3],"min", ys.min(), "max", ys.max(), "µ", ys.mean(), "s", ysig

    # plot data points
    plt.figure(1)
    data = []

    plt.subplot(221)
    data = [(x, y) for x in xs if x < xcutoff for y in ys if y >= ycutoff]
    xl, yl = numpy.array(get_bounded(xs, ys, 0, xcutoff, ycutoff, ys.max()))
    print plt.axis()
    plt.plot(xl, yl, 'k.')

    plt.subplot(222)
    xl, yl = numpy.array(get_bounded(xs, ys, xcutoff, xs.max(), ycutoff, ys.max()))
    print plt.axis()
    plt.plot(xl, yl, 'b.')

    plt.subplot(223)
    xl, yl = numpy.array(get_bounded(xs, ys, 0, xcutoff, 0, ycutoff))
    print plt.axis()
    plt.plot(xl, yl, 'r.')


    plt.subplot(224)
    xl, yl = numpy.array(get_bounded(xs, ys, xcutoff, xs.max(), 0, ycutoff))
    print plt.axis()
    plt.plot(xl, yl, 'g.')

    plt.show()
