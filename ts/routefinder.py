#!/usr/bin/env python
	
import math, random
from util import Vector
import data

rsizes = [0 for i in range(50)]
res = []

def print_end(): 
	for i, e in enumerate(rsizes):
		print i, e

class RouteFinder:

	#this returns the result in *string* format, not numbers...
	def findroute(self, journeys, stime, etime):
		
		total_time = etime - stime
		if not journeys or total_time == 0:
			return False


		#find the total distance first
		total_dist = 0
		for line, journey in journeys:

			start, end = data.getstartend(line, journey[0], journey[-1])
			
			for i in range(start, end):
				s, e = i, i+1 #intermediate start, end
				total_dist+= (data.positions[line][s] - data.positions[line][e]).mag()
				
		if total_dist == 0.0:
#			print "NO 1"
			return False
		speed = total_dist/total_time

			
		last, dist = Vector(), 0
		linesandpoints = []
		
		for line, journey in journeys:
			
			start, end = data.getstartend(line, journey[0], journey[-1])

			p = [(data.positions[line][start], dist/speed+stime)]
			
			for i in range(start, end):
				s, e = i, i+1 
				direction = data.positions[line][s] - data.positions[line][e]
				dist+= direction.mag()
				
				
				#if the direction of the new direction is 
				#almost the same as the old, replace the old with new
				#try:
				#print start_station, end_station, direction.angle(last)
				if direction.angle(last) < 0.1 and len(p) > 0:
					p[-1] = (data.positions[line][e], dist/speed+stime)
				else:
					p.append((data.positions[line][e], dist/speed+stime))
				# except Exception as e:
				# 	print "NO 2", e
				# 	return False
				

				last = direction
			
			linesandpoints.append((line, p))
		
		
		results = []

		#data = 1 + 3 + (12*3) = 
		
		for line, route in linesandpoints:


			result = ["0.0f:0.0f,0.0f" for i in range(12)]
			t = stime
# 			print route
			rsizes[len(route)]+= 1
			
			# if len(route) > 12:
			# 	print "* * * * * * JOURNEY TOO LONG * * * * * * ", "(%i)" % (len(result))
			# 	# print "{", route[0][0].x , ",", route[0][0].y , "},"
			# 	# for i, point in enumerate(route):
			# 	# 	if i > 0:
			# 	# 		print "{", point[0].x , ",", point[0].y , "},"

			# 	return False
			
			
			for i, point in enumerate(route):
				if i > 0 and not i > 11:
					result[i-1] = "%.2ff:%.2ff,%.2ff" % (point[1], point[0].x, point[0].y)
					#print "{", point[0].x , ",", point[0].y , "},"
			
			#try:
			strres = "%i|%.1ff:%.1ff,%.1ff>%s" % (data.encodeline(line[:-1]), route[0][1], route[0][0].x, route[0][0].y, ";".join(result))
			results.append(strres)
			#except Exception as e:
				# print 233, e
				# return False
			
		
		return results
		
# 		for result in results:
# 					
# 			
# 		
# 		try:
# 			return "%.1ff:%.1ff,%.1ff>%s" % (stime, self.stations[journey[0]].x, self.stations[journey[0]].y, ";".join(result))
# 		except:
# 			return False
			
