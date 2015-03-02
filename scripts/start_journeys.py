#!/usr/bin/env python

import sys

from journeyplanner import JourneyPlanner
from routefinder import *
import data
import time, sys

beg = time.clock()

jp = JourneyPlanner()
rf = RouteFinder()

result = open("start_"+sys.argv[1], 'w')
p = True if len(sys.argv) > 2 else False
done, i = 0, 0

line_cols = {
    'Bakerloo': (137, 78, 36),
    'Central': (220, 36, 31),
    'Circle': (255, 206, 0),
    'District': (0, 114, 41),
    'Hammersmith&City': (215, 153, 175),
    'Jubilee': (134, 143, 152),
    'Metropolitan': (117, 16, 86),
    'Northern': (0, 0, 0),
    'Piccadilly': (0, 25, 168),
    'Victoria': (0, 160, 226),
    'Waterloo&City': (118, 208, 189),
}

w = 1123
h = 750
# poses = [(i, j) for i in range(w) for j in range(h)]
# pixels = [(255,)*3 for i in range(len(poses))]

# print 'loading pickle'
# import cPickle
# pixels, poses = cPickle.load(open('pix_data.pickle'))

# print 'done in', (time.clock() - beg)

from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient()
db = client.geo
spatialtwo = db.spatialtwo
# listings = db.core_listings


import kdtree

tc = time.time()
print 'initialising kdtree'
tree = kdtree.create(poses)
print 'done in %2.2f' % (time.time()-tc)

# cPickle.dump(tree, open('tree.pickle', 'wb'))


# line_nums = dict([(e, i) for i, e in enumerate(stations_positions.keys())])
segs = time.time()

with open(sys.argv[1], 'r') as f:
    try:
        for line in f:
            tokens = line.split(',')
            journeys =  jp.journey(tokens[3][1:-1], tokens[4][1:-1])
            if journeys:
                station = journeys[0][1][0]
                line = journeys[0][0][:-1]
                pos = data.stations[station].pos
                # print done, station, line, line_cols[line], #line_nums[line]
                # data.station

                t = time.time()
                p = tree.search_nn(pos)
                tt = time.time() - t
                print tt, ' ',
                x, y = p.data
                pixels[y*w+x] = line_cols[line]
                tree = tree.remove(p.data)
                # print '%2.2f' % (time.time() - t)
                print time.time()-t-tt
                done+= 1

                if done % 1000 == 0:
                    print '\n%d: %2.4f' % (done, time.time()-segs)
                    segs = time.time()

                sys.stdout.write("\rdone: %d" % (done))
                sys.stdout.flush()
                
                # if done % 6000 == 0:
                #     print 'rebalancing'
                #     t = time.time()
                #     tree = tree.rebalance()
                #     print time.time() - t

                # result.write('%s;%s\n' % (journeys[0][1][0], journeys[0][0][:-1]))
                # i+= 1
            # route = rf.findroute(journeys, int(tokens[5][1:-1]), int(tokens[7][1:-1]))
            # if route:
            #     for r in route:
            #         result.write(r + "\n")
            #     if(p): print tokens[3][1:-1], "->", tokens[4][1:-1]
                # i+= 1
                # done+= 1

    except KeyboardInterrupt:
        print 'quiting'
        pass
        # sys.stdout.write("\rdone: %d, failed: %d, fail rate: %2.2f%%" % (done, done-i, (done-i)/float(done)*100.0))
        # sys.stdout.flush()


import PIL.Image as Image
img = Image.new('RGB', (w, h))
img.putdata(pixels)
img.save('out%s.png' % (done))

# d = (pixels, [x.data for x in tree.inorder()])
# cPickle.dump(d, open('pix_data.pickle', 'wb'))

# print_end()
sys.stdout.write("\n")
result.close()
# with open("distr", 'w') as f:
#     for i,j in enumerate(distr):
#         f.write("%i,%i\n" % (i, j))
    
# print "completed in %.2fs" % ()
print "-\ndone %i in %2.2f" % (done, (time.clock() - beg))
