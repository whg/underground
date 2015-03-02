import math, random
from util import Vector
import data
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class RouteFinder(object):

   #this returns the result in *string* format, not numbers...
    def findroute(self, journeys, stime, etime):
      
        total_time = etime - stime
        if not journeys or total_time == 0:
            logger.info('no journey')
            return False


        total_dist = 0
        for line, journey in journeys:

            start, end = data.getstartend(line, journey[0], journey[-1])
            inc = 1 if (end > start) else -1
            for i in range(start, end, inc):
                s, e = i, i+inc #intermediate start, end
                total_dist+= (data.positions[line][s] - data.positions[line][e]).mag()
            
        if total_dist == 0.0:
            logger.info('total dist = 0')
            return False
            
        speed = total_dist/total_time

        
        if speed > 30:
            logger.info('massive speed!')
            return False
         
        last, dist = Vector(), 0
        linesandpoints = []
      
        for line, journey in journeys:
         
            start, end = data.getstartend(line, journey[0], journey[-1])

            pos = data.positions[line][start]
            p = [[pos.x, pos.y, dist/speed+stime]]
            # p = [(data.positions[line][start], dist/speed+stime)]
            inc = 1 if end > start else -1
            for i in range(start, end, inc):
                s, e = i, i+inc
                direction = data.positions[line][s] - data.positions[line][e]
                dist+= direction.mag()
            
            
                #if the direction of the new direction is 
                #almost the same as the old, replace the old with new
                #try:
                #print start_station, end_station, direction.angle(last)
                pos = data.positions[line][e]
                v = [pos.x, pos.y, dist/speed+stime]

                if direction.angle(last) < 0.1 and len(p) > 1:
                    p[-1] = v
                else:
                    p.append(v)

                last = direction

            linesandpoints.append((line, p))
      

        results = []
      
        for line, route in linesandpoints:

            if len(route) > 12:
                continue

            results.append((data.line_colour(line[:-1]), route + [[0,0,0]]*(12-len(route))))
      
        return results
