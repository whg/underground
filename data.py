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
        with open("./data/lines/%s.txt" % line, 'r') as g:
            lines[line] = [l.strip() for l in g.readlines()]

        #postions: positions of all points in line, including between
        #stations position_indices: index of each station in points,
        #we need this because of the intermediate points
        with open("./data/map/%s.txt" % line, 'r') as g:
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
    try:
        start_index = position_indices[line][start_station]
        end_index = position_indices[line][end_station]
    except KeyError:
        print line, start_station, end_station
        raise KeyError
    
    # start = min(start_index, end_index)
    # end = max(start_index, end_index)

    return (start_index, end_index)

#add postions to stations
for line, _stations in position_indices.items():
    for station, index in _stations.items():
        p = positions[line][index]
        stations[station].pos = (p.x, p.y)



_line_colors = {
    'Bakerloo': (153, 90, 9),
    'Central': (255, 73, 0),
    'Circle': (255, 230, 0),
    'District': (0, 170, 107),
    'Hammersmith&City': (255, 128, 161),
    'Jubilee': (133, 134, 136),
    'Metropolitan': (121, 0, 43),
    'Northern': (36, 36, 36),
    'Piccadilly': (32, 0, 161),
    'Victoria': (0, 159, 228),
    'Waterloo&City': (77, 207, 186),
}

def line_colour(line):
    v = _line_colors[line]
    return [w/255.0 for w in v]
    
