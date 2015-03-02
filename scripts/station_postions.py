import data
import sys
import cPickle

if len(sys.argv) < 2:
    print 'need file'
    exit()

poses = map(lambda e: data.stations[e.strip()].pos, open(sys.argv[1]))
# print poses

cPickle.dump(poses, open('positions.pickle', 'wb'))

# with open(sys.argv[1], 'r') as f:
#     for line in f:
#         pos = data.stations[line.strip()].pos
#         print pos

