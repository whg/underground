#!/usr/bin/env python

import sys

from journeyplanner import JourneyPlanner
from routefinder import *
import time, sys

beg = time.clock()

jp = JourneyPlanner()
rf = RouteFinder()

result = open("result"+sys.argv[1], 'w')
p = True if len(sys.argv) > 2 else False
done, i = 0, 0


with open(sys.argv[1], 'r') as f:
    for line in f:
        tokens = line.split(',')
        journeys =  jp.journey(tokens[3][1:-1], tokens[4][1:-1])
        print journeys[0][0][:-1]
        route = rf.findroute(journeys, int(tokens[5][1:-1]), int(tokens[7][1:-1]))
        if route:
            for r in route:
                result.write(r + "\n")
            if(p): print tokens[3][1:-1], "->", tokens[4][1:-1]
            i+= 1
        done+= 1

        # sys.stdout.write("\rdone: %d, failed: %d, fail rate: %2.2f%%" % (done, done-i, (done-i)/float(done)*100.0))
        # sys.stdout.flush()



# print_end()
sys.stdout.write("\n")
result.close()
# with open("distr", 'w') as f:
#     for i,j in enumerate(distr):
#         f.write("%i,%i\n" % (i, j))
    
# print "completed in %.2fs" % ()
print "-\ndone in %2.2f" % ((time.clock() - beg))
