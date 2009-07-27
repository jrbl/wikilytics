#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""JData - a simple statistical data modeling class, abstracting away some of SciPy

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

import sys
import numpy, scipy, scipy.linalg

DEBUG = True
EPSILON = 1e-8                         # maximum distance w/in which we consider two things equal

#########################################################################################
# A class to represent data and to do PCA:
#   FIXME: incomplete; copy in additional functionality from below

class JData(object):
    """Models the behavior of some pile of data."""

    def __init__(self, fileURL = "data.csv", compCount = -1):
        """FIXME: Use reset() to avoid code reproduction."""
        self._headings = []
        self._names    = []
        self.means     = []
        self.sigmas    = []

        data = self._getSomeData(fileURL)        # 1
        self.data = data
        norm_data = self._subtractTheMeans()     # 2
        self.norm_data = norm_data
        covariance = numpy.cov(norm_data)        # 3
        self.covariance = covariance
        eigValues, eigVectors = scipy.linalg.eig(covariance) # 4
        components = self._chooseComponents(eigValues, eigVectors, compCount)   # 5
        self.components = components
        self.eigenVectors = eigVectors
        self.eigenValues = eigValues

        self.sigmas                       = [numpy.sqrt(numpy.var(col)) for col in data]
        sum_of_variances                  = sum([x*x for x in self.sigmas])
        #self.componentVariancePercentages = [abs(x) / abs(sum(eigValues)) for x in eigValues]
        self.componentVariancePercentages = [abs(numpy.var(x)) / sum_of_variances for x in data]
        self.labeledComponents            = [self._headings[x+1] for x in components]

    def _getSomeData(self, fileURL = "data.csv"): # STEP 1
        """Read in a CSV, scrubbing input for sanity as we go.  Cast everything to floats.
                         
        Open from an arbitrary URL, stow away the first (column title) row's data.  Throw away
        rows with a different number of columns.

        FIXME: reads everything into memory.  Pipelining requires multiple passes, though, and our
               dataset is (currently) small.
        """
        import csv
        fileHandle = numpy.DataSource().open(fileURL)
        rdr = csv.reader(fileHandle)
        input = []
        for row in rdr:
            if (len(self._headings) == 0):          # filter 0th row
                self._headings = row
                continue
            elif (len(row) != len(self._headings)): # filter weird rows
                continue
            else:
                for x in range(len(row)):     # floatify all numeric values
                    if (x == 0):              # ...except the data label!
                        self._names.append(row[x])                                             
                        continue  
                    row[x] = float(row[x])
                input.append(row[1:])         # leave label out of dataset
        
        fileHandle.close()
        return numpy.atleast_1d(input).transpose()

    def _subtractTheMeans(self): # STEP 2
        """Return a copy of input with the means of each column subtracted out."""
        import copy
        data = copy.deepcopy(self.data)
        for i in range(len(data)):
            mu = data[i].mean()
            self.means.append(mu)
            data[i] = data[i] - mu
        return data

    def _chooseComponents(self, eigenvalues, eigenvectors, n = -1): # STEP 5
        """Choose first n principal components and return a feature vector.
                                                                
        If n is negative, return all components.
        """
        original_eigVals = eigenvalues.tolist()
        eigenvalues = sorted(eigenvalues, reverse=True)
        indices = [original_eigVals.index(x) for x in eigenvalues]
        if (n < 1):
            return indices
        return indices[:n]

    def reset(self, nparray, compCount = -1):
        """Use nparray as the data table and recalculate all our stats.

        To use a numpy array as a source instead of a file, create the JData object with
        filename None, and then call reset with the name of the numpy array.
        """
        self._headings = []
        self._names    = []
        self.means    = []

        self.data = nparray                      # 1
        norm_data = self._subtractTheMeans()     # 2
        self.norm_data = norm_data
        covariance = numpy.cov(norm_data)        # 3
        self.covariance = covariance
        eigValues, eigVectors = scipy.linalg.eig(covariance) # 4
        components = self._chooseComponents(eigValues, eigVectors, compCount)   # 5
        self.components = components
        if self._headings:
            self.labeledComponents = [self._headings[x+1] for x in components]
        self.componentVariancePercentages = [abs(x) / abs(sum(eigValues)) for x in eigValues]
        self.eigenVectors = eigVectors
        self.eigenValues = eigValues




#########################################################################################
# Test harness from here on out

def test_ObjectAllComponents():
    """Processes a data set and retrieves all of its components.  Output == Input?

    Goes through a complete PCA breakdown, retrieving all components in the dataset, and
    going through the data recovery process.  What comes out the other side should be
    within EPSILON of what was put in, or else we've done something terribly wrong.

    This can also be used as a recipe for performing a real PCA.
    """
    data = JData("data.csv", -1)
    eVecs = data.eigenVectors
    features = [eVecs[x].tolist() for x in data.components] # Step 5.5: building feature matrix
    features = numpy.atleast_1d(features)
    if (len(features) == 1):
        features = features.flatten()

    finalData = numpy.inner(features.transpose(), data.norm_data.transpose()) # Step 6
    dataRecovery = numpy.inner(features, finalData.transpose())
    for i in range(len(dataRecovery)):
        mu = data.means[i]
        dataRecovery[i] = dataRecovery[i] + mu

    deltas = abs(dataRecovery - data.data)
    return (deltas.max() <= EPSILON)


if __name__ == "__main__":

    print "test_AllComponents: ",
    if test_ObjectAllComponents():
        print "OK"
    else: 
        print "FAILURE"
        sys.exit()

    d = JData("data.csv", 3)
    print d.labeledComponents
