#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################################

"""anonymize anonymizes a CSV data set conforming to our expectations.
Copyright (C) 2009  Joe Blaylock <jrbl@jrbl.org>

Our expectations:
* Subjects are by row, individual statistics are by column
* Subject names are in col 0
* Row 0, Col 0 is a column title that we can change
* row order doesn't matter, as long as columnar integrity is preserved
* column order doesn't matter, as long as row integrity is preserved

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

import os
import csv
import random
import uuid

supersecret = []

def changeFirstField(line, val, sep=',', quote=True):
    zero_end = line.find(sep)
    supersecret.append(line[0:zero_end])
    line = line[zero_end:]
    if quote:
        val = '"' + str(val) + '"'
    line = str(val) + line
    return line

if __name__ == "__main__":
    """Read in a CSV and anonymize it.
                     
    Store the first row as headings; change 0,0 to "UUID".  Change the first column's data 
    to a UUID.  

    Reads everything into memory, which may not be the right thing for large datasets, but
    makes randomizing the rows very easy.
    """
    #fileHandle = DataSource().open(fileURL) # requires numpy.DataSource; gets from URL
    fileHandle = open('NOMINIZED.csv')
    contents = fileHandle.readlines()
    headers = contents[0]
    contents = contents[1:]
    random.shuffle(contents)

    headers = changeFirstField(headers, "UUID")
    for i in range(len(contents)):
        contents[i] = changeFirstField(contents[i], uuid.uuid4())

    contents.insert(0, headers)

    fileHandle.close()
    fileHandle = open(os.pardir + os.sep + 'data.csv', 'w')
    fileHandle.writelines(contents)
    fileHandle.close()

    fileHandle = open(os.curdir + os.sep + 'RENOMINIZED.csv', 'w')
    fileHandle.write("This is the list of names trimmed from the NOMINIZED.csv to create data.csv.\n")
    fileHandle.write("The items are ordered in the same way as the rows of data.csv.  To retrieve\n")
    fileHandle.write("NOMINIZED.csv, substitute these names back in for those, and alphabetize.\n\n")
    for name in supersecret:
        fileHandle.write(name+"\n")
    fileHandle.close
    os.chmod(os.curdir + os.sep + 'RENOMINIZED.csv', 000)
