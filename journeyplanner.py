#!/usr/bin/env python

import random
import data
from util import *

class JourneyPlanner:
	'''read files with data and then can plan a route for you
	this is a slightly weird journey planner as i wanted to preserve
	the lines used in a journey, so it's not truly a graph we working with
	'''

	def __init__(self):
		self.shortestlen = 0
		
	# def __init__(self):			
	# 	self.lines = dict()
	# 	self.stations = dict()
	# 	self.loadstationdata()
	# 	self.shortestlen = 0

	# def loadstationdata(self):
	# 	#read the line files, and load the data
	# 	with open("./data/line_names", 'r') as f:	
	# 		line_names = [l.strip() for l in f.readlines()]
			
	# 		for line in line_names:
	# 			with open("./data/"+line, 'r') as g:
	# 				self.lines[line] = [l.strip() for l in g.readlines()]
		
	# 	#work out which lines go through each station	
	# 	for l, sts in self.lines.iteritems():
	# 		for station in sts:
	# 			if station in self.stations:
	# 				self.stations[station].lines.append(l)
	# 			else:
	# 				self.stations[station] = Station(station, [l])
		
	# 	#add the positions to each station
	# 	with open("data/stations_position", 'r') as f:
	# 		for line in f:
	# 			st, p = line.split(':')
	# 			x,y,z = p.split(',')
	# 			if st in self.stations:
	# 				self.stations[st].loc = (float(x), float(y))
		
	# #this helper calculates distance between two stations
	# def dist(self, s1, s2):
	# 	x = (self.stations[s1].loc[0] - self.stations[s2].loc[0])**2
	# 	y = (self.stations[s1].loc[1] - self.stations[s2].loc[1])**2
	# 	#no need for expensive square root....
	# 	return (x+y)*1000 #mult by 1000 for easy reading
	
	
	# FINDROUTE
	#returns all possible paths with a maximum of 2 changes
	def findjourney(self, start, end, journey=[]):
		
		journey = journey + [start]
		routes = []
		
		for line in data.stations[start].lines:
			if end in data.lines[line]:
				journey.extend([line, end])
				return [journey]
			
			for station in data.lines[line]:
				if station not in journey and line not in journey:
					
					#hack 1: max 2 changes
					if len(journey) > 3:
						continue
					
					new = self.findjourney(station, end, journey+[line])
					for j in new:
						if j not in routes:
							routes.append(j)
							
							#hack 2: if this has fewer stops than what we have seen before,
							#use it, this is not optimal but creates a substantial speed increase
							l = len(j)
							if l < self.shortestlen:
								return [j]
							self.shortestlen = l
						
		return routes
	
	
	def journey(self, source, dest):
		
		#find routes with duplicate lines
		routes = self.findjourney(source, dest)	
		paths = []
		
		for path in routes:
			
			#remove the number from the end of the lines...
			pp = path[:]
			for i in range(len(path[1::2])):
				pp[i*2+1] = path[i*2+1][0:-1]
				
			#...then make sure we haven't done this line already
			if pp not in [ae.route for ae in paths]:
				
				#make a list of tuples with a start and end tuple, 
				#and the line, i like python
				pairs = zip(path[0::2], path[2::2])
				lns = path[1::2]
				j = zip(pairs, path[1::2])
				
				d = 0
				stops = []
				sjns = []
				
				for st, line in j:	
					start = data.lines[line].index(st[0])
					end = data.lines[line].index(st[1])
					
					#add the distance between each stop
					for i in range(min([start, end]), max([start, end])-1):
						d+= data.dist(data.lines[line][i], data.lines[line][i+1])
						
					if (end - start) < 0:
						t = data.lines[line][end:start+1]
						t.reverse()
					else:
						t = data.lines[line][start:end+1]
					
					stops.extend(t)		
					#sjns.append((int("%i%s" % (util.encodeline(line[0:-1]), line[-1:])), t))
					sjns.append((line, t))
					
				#remove the number from the line
				for i in range(len(lns)):
					path[i*2+1] = path[i*2+1][0:-1]
				
				#add the line 
				paths.append(Journey(path, stops, len(lns)-1, d, sjns))
		
		
		#sort according to rank
		paths.sort(key=lambda x: x.rank)
		paths = paths[0:3]
		
# 		if len(paths) > print "\t", paths[0].route
		
		#now we have a sorted list
		#split the journey into all the seperate lines
		
		if len(paths) < 1:
			return False
		else:
			print paths[0].sjns
			return paths[0].sjns
		if len(paths) == 1:
			return paths[0].stops
		elif len(paths) == 2:
			return paths[int(random.random()*2)].stops
		else:
			return paths[int(random.random()*3)].stops
