#!/usr/bin/env python
	
import math, random
from util import Vector

rsizes = [0 for i in range(50)]

def print_end(): 
	for i, e in enumerate(rsizes):
		print i, e

class RouteFinder:
	def __init__(self):
		self.stations = dict()
		self.loaddata()
		
	def loaddata(self):
		with open("data/map_pos", 'r') as f:
			for line in f:
				st, p = line.split(':')
				x,y = p.split(',')
				self.stations[st] = Vector(float(x), float(y))
	
	#this returns the result in *string* format, not numbers...
	def findroute(self, journeys, stime, etime):
		
		total_time = etime - stime
		if not journeys or total_time == 0:
			return False


		#find the total distance first
		total_dist = 0
		for line, journey in journeys:
			for s, e in zip(journey[:-1], journey[1:]):
				total_dist+= (self.stations[s] - self.stations[e]).mag()
		
		if total_dist == 0.0: return False
		speed = total_dist/total_time

			
		last = Vector()
		points = []
		dist = 0
		lines = []
		
# 		print zip(journey[:-1], journey[1:])
		for line, journey in journeys:
			p = [(self.stations[journey[0]], dist/speed+stime)]
			lines.append(line)
			for s, e in zip(journey[:-1], journey[1:]):
				if s == e:
					continue
				
				direction = self.stations[e] - self.stations[s] 
				dist+= direction.mag()
				
				
				#if the direction of the new direction is 
				#almost the same as the old, replace the old with new
				try:
					if direction.angle(last) < 0.1 and len(p) > 0:
# 						if len(p) > 0: 
						p[-1] = (self.stations[e], dist/speed+stime)
# 						else:
# 							p.append((self.stations[e], dist/speed+stime))
					else:
						p.append((self.stations[e].addnoise(), dist/speed+stime))
				except:
					return False		

				last = direction
			points.append(p)
		
		
		results = []
		for route, line in zip(points, lines):
			result = ["0.0f:0.0f,0.0f" for i in range(12)]
			t = stime
# 			print route
			rsizes[len(route)]+= 1
			if len(route) > 12:
# 				print "* * * * * * JOURNEY TOO LONG * * * * * * ", "(%i)" % (len(result))
				return False

			for i, point in enumerate(route):
				if i > 0:
					result[i-1] = "%.2ff:%.2ff,%.2ff" % (point[1], point[0].x, point[0].y)
			
			try:
				strres = "%i|%.1ff:%.1ff,%.1ff>%s" % (util.encodeline(line[:-1]), route[0][1], route[0][0].x, route[0][0].y, ";".join(result))
				results.append(strres)
			except Exception as e:
				print 2, e
				return False
			
		
		return results
		
# 		for result in results:
# 					
# 			
# 		
# 		try:
# 			return "%.1ff:%.1ff,%.1ff>%s" % (stime, self.stations[journey[0]].x, self.stations[journey[0]].y, ";".join(result))
# 		except:
# 			return False
			
