lines = ["Bakerloo",
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

def encodeline(linename):
    return lines.index(linename)

def decodeline(linenumber):
    return lines[linenumber]
