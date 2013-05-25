#!/usr/bin/env python

import random

#something to store station data
class Station:
	def __init__(self, name, lines=[], loc=(0,0)):
		self.name = name
		self.lines = lines
		self.loc = loc

class Journey:
	def __init__(self, route=[], stops=[], changes=0, dist=0, sjns=[]):
		#route: [start, (line, intermediate_station)*, line, end]
		self.route = route
		#stops: [start, station*, end]
		self.stops = stops
		#number of changes
		self.changes = changes
		#sum of as the crow flies distance between stops
		self.dist = dist
		#a simple ranking...
		self.rank = len(stops) * (changes+1) * dist
		#separate journeys
		self.sjns = sjns
# 		print "yo"


class JourneyPlanner:
	'''read files with data and then can plan a route for you
	this is a slightly weird journey planner as i wanted to preserve
	the lines used in a journey, so it's not truly a graph we working with
	'''
	
	def __init__(self):			
		self.lines = dict()
		self.stations = dict()
		self.loadstationdata()
		self.shortestlen = 0

	def loadstationdata(self):
		#read the line files, and load the data
		with open("./data/line_names", 'r') as f:	
			line_names = [l.strip() for l in f.readlines()]
			
			for line in line_names:
				with open("./data/"+line, 'r') as g:
					self.lines[line] = [l.strip() for l in g.readlines()]
		
		#work out which lines go through each station	
		for l, sts in self.lines.iteritems():
			for station in sts:
				if station in self.stations:
					self.stations[station].lines.append(l)
				else:
					self.stations[station] = Station(station, [l])
		
		#add the positions to each station
		with open("data/stations_position", 'r') as f:
			for line in f:
				st, p = line.split(':')
				x,y,z = p.split(',')
				if st in self.stations:
					self.stations[st].loc = (float(x), float(y))
		
	#this helper calculates distance between two stations
	def dist(self, s1, s2):
		x = (self.stations[s1].loc[0] - self.stations[s2].loc[0])**2
		y = (self.stations[s1].loc[1] - self.stations[s2].loc[1])**2
		#no need for expensive square root....
		return (x+y)*1000 #mult by 1000 for easy reading
	
	
	# FINDROUTE
	#returns all possible paths with a maximum of 2 changes
	def findjourney(self, start, end, journey=[]):
		
		journey = journey + [start]
		routes = []
		
		for line in self.stations[start].lines:
			if end in self.lines[line]:
				journey.extend([line, end])
				return [journey]
			
			for station in self.lines[line]:
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
	
	def encodeline(self, line):
		if line == "Bakerloo": return 0
		elif line == "Central": return 1
		elif line == "Circle": return 2
		elif line == "District": return 3
		elif line == "Hammersmith&City": return 4
		elif line == "Jubilee": return 5
		elif line == "Metropolitan": return 6
		elif line == "Northern": return 7
		elif line == "Piccadilly": return 8
		elif line == "Victoria": return 9
		elif line == "Waterloo&City": return 10
	
	def journey(self, source, dest):
		
		#find routes with duplicate lines
		routeswd = self.findjourney(source, dest)	
		
# 		print routeswd
# 		for i in routeswd: print len(i), i
		
		#now remove the duplicates, i.e:
		#['Gloucester Road', 'District5', 'Earls Court', 'District3', 'Acton Town']
		# routes = []
		# for r in routeswd:
		# 	lns = [l[0:-1] for l in r[1::2]]
		# 	dup = False
		# 	for l in lns:
		# 		if lns.count(l) > 1:
		# 			dup = True
		#  			break
		#  	if not dup:
		#  		routes.append(r)
		routes = routeswd
				
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
					start = self.lines[line].index(st[0])
					end = self.lines[line].index(st[1])
					
					#add the distance between each stop
					for i in range(min([start, end]), max([start, end])-1):
						d+= self.dist(self.lines[line][i], self.lines[line][i+1])
						
					if (end - start) < 0:
						t = self.lines[line][end:start+1]
						t.reverse()
					else:
						t = self.lines[line][start:end+1]
					
					stops.extend(t)		
					sjns.append((int("%i%s" % (self.encodeline(line[0:-1]), line[-1:])), t))
					
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
			print paths[0].stops
			return paths[0].sjns
		if len(paths) == 1:
			return paths[0].stops
		elif len(paths) == 2:
			return paths[int(random.random()*2)].stops
		else:
			return paths[int(random.random()*3)].stops
