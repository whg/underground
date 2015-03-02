#!/usr/bin/env python

import sys

from journeyplanner import journey
from routefinder import findroute
import time, sys
from array import array
from itertools import chain
import data
import cPickle
import logging
import os

logging.basicConfig()

beg = time.clock()

p = True if len(sys.argv) > 2 else False
p = False
suf = '' if not len(sys.argv) > 2 else sys.argv[2]
done, i = 0, 0

lists = [] #[[]]*8
cols = []

infospacing = 10
outputdir = 'output'

with open(sys.argv[1], 'r') as f:
    for line in f:
        tokens = line.split(',')

        journeys =  journey(tokens[3][1:-1], tokens[4][1:-1])
        route = findroute(journeys, int(tokens[5][1:-1]), int(tokens[7][1:-1]))
        
        if route:
            for line_col, j in route:
                cols+= line_col
                lists+= [j]

            if(p): print tokens[3][1:-1], "->", tokens[4][1:-1] #, '(%s)' % data.decodeline(int(r[0]))
            i+= 1
        done+= 1

        if i % infospacing == 0:
            sys.stdout.write("\rdone: %d, failed: %d, fail rate: %2.2f%%" % (done, done-i, (done-i)/float(done)*100.0))
            sys.stdout.flush()

print

#write all the position data
for i, z in enumerate(zip(*lists)):
    with open(os.path.join(outputdir, 't%d%s.data' % (i, suf)), 'wb') as f:
        a = array('f', chain(*z))
        a.tofile(f)

#write colour data
with open(os.path.join(outputdir, 'cols.data%s' % suf), 'wb') as f:
    array('f', cols).tofile(f)

print 'wrote a total of', len(cols), 'journeys'

print "-\ncompleted in %2.2f" % ((time.clock() - beg))
