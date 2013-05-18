#!/usr/bin/env python

import sys

from journeyplanner import JourneyPlanner
from routefinder import RouteFinder
import time
beg = time.clock()

jp = JourneyPlanner()
rf = RouteFinder()

result = open("result"+sys.argv[1], 'w')

i = 0


with open(sys.argv[1], 'r') as f:
	for line in f:
		tokens = line.split(',')
		journeys =  jp.journey(tokens[3][1:-1], tokens[4][1:-1])
		route = rf.findroute(journeys, int(tokens[5][1:-1]), int(tokens[7][1:-1]))
		if route:
			for r in route:
				result.write(r + "\n")
			print i, tokens[3][1:-1], tokens[4][1:-1]
			
		i+= 1



 		
result.close()
# with open("distr", 'w') as f:
# 	for i,j in enumerate(distr):
# 		f.write("%i,%i\n" % (i, j))
	
print "completed in %.2fs" % ((time.clock() - beg))
