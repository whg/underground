#!/usr/bin/env python

import sys

from journeyplanner import JourneyPlanner
from routefinder import *
import time, sys
from array import array
from itertools import chain
import data
import cPickle

beg = time.clock()

jp = JourneyPlanner()
rf = RouteFinder()

# result = open("result"+sys.argv[1], 'w')
p = True if len(sys.argv) > 2 else False
p = False
suf = '' if not len(sys.argv) > 2 else sys.argv[2]
done, i = 0, 0

lists = [] #[[]]*8
cols = []
ses = []

with open(sys.argv[1], 'r') as f:
    for line in f:
        tokens = line.split(',')
        journeys =  jp.journey(tokens[3][1:-1], tokens[4][1:-1])
        # print journeys[0][0][:-1]
        route = rf.findroute(journeys, int(tokens[5][1:-1]), int(tokens[7][1:-1]))
        if route:
            # ses.extend(route)
            for line_col, j in route:
                # pass
                cols+= line_col
                lists+= [j]
                # result.write(r + "\n")
            if(p): print tokens[3][1:-1], "->", tokens[4][1:-1] #, '(%s)' % data.decodeline(int(r[0]))
            i+= 1
        # else:
            # print route, tokens[3][1:-1], tokens[4][1:-1]
            # print line
        done+= 1

        sys.stdout.write("\rdone: %d, failed: %d, fail rate: %2.2f%%" % (done, done-i, (done-i)/float(done)*100.0))
        sys.stdout.flush()


# cPickle.dump(ses, open('ses.pickle', 'wb'))
# print 'ses:', ses

# print_end()
# print
# print lists
# print
for i, z in enumerate(zip(*lists)):
    with open('t%d%s.data' % (i, suf), 'wb') as f:
        a = array('f', chain(*z))
        a.tofile(f)
    # print(zip(*lists))


with open('cols.data%s' % suf, 'wb') as f:
    array('f', cols).tofile(f)
    print len(cols)

# sys.stdout.write("\n")
# result.close()
# with open("distr", 'w') as f:
#     for i,j in enumerate(distr):
#         f.write("%i,%i\n" % (i, j))
    
# print "completed in %.2fs" % ()
print "-\ndone in %2.2f" % ((time.clock() - beg))
