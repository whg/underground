from util import *

lines = dict()
stations = dict()
linenames = ["Bakerloo",
             "Central",
             "Circle",
             "District",
             "Hammersmith&City",
             "Jubilee",
             "Metropolitan",
             "Northern",
             "Piccadilly",
             "Victoria",
             "Waterloo&City"]
position_indices = dict()
positions = dict()

with open("./data/line_names", 'r') as f:	
    line_names = [l.strip() for l in f.readlines()]
    
    for line in line_names:
        with open("./data/" + line, 'r') as g:
            lines[line] = [l.strip() for l in g.readlines()]

        #postions: positions of all points in line, including between
        #stations position_indices: index of each station in points,
        #we need this because of the intermediate points
        with open("./data/map/" + line, 'r') as g:
            points = eval('[' + g.read() + ']')
            position_indices[line] = dict()
            positions[line] = []
            i = 0
            for j, (v, p) in enumerate(points):
                if v == 's':
                    station = lines[line][i]
                    position_indices[line][station] = j
                    i+= 1
                positions[line].append(Vector(p))
                
            
    #work out which lines go through each station	
    for l, sts in lines.iteritems():
        for station in sts:
            if station in stations:
                stations[station].lines.append(l)
            else:
                stations[station] = Station(station, [l])

    
                
#add the positions to each station
with open("data/stations_position", 'r') as f:
    for line in f:
        st, p = line.split(':')
        x,y,z = p.split(',')
        if st in stations:
            stations[st].loc = (float(x), float(y))

            
def dist(s1, s2):
    '''manhattan distance'''
    x = (stations[s1].loc[0] - stations[s2].loc[0])
    y = (stations[s1].loc[1] - stations[s2].loc[1])
    return (x+y)*1000 #mult by 1000 for easy reading


def encodeline(linename):
    return linenames.index(linename)

def decodeline(linenumber):
    return linenames[linenumber]

def getstartend(line, start_station, end_station):
    start_index = position_indices[line][start_station]
    end_index = position_indices[line][end_station]
    
    # start = min(start_index, end_index)
    # end = max(start_index, end_index)

    return (start_index, end_index)

#add postions to stations
for line, _stations in position_indices.items():
    for station, index in _stations.items():
        stations[station].pos = positions[line][index]
