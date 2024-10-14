import pandas as pd
import json
import math

def differenzZwischenZweiPunkten(lat1,lon1,lat2,lon2):
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2-lat1)
    delta_lambda = math.radians(lon2-lon1)

    a = math.sin(delta_phi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    distance = R * c
    return distance

haltestellen = pd.read_excel("data/HVV-Haltestellen.xlsx", header = 0)


with open("data/anliegen_extern.json", 'r', encoding='utf-8') as datei:
    meldungen = json.load(datei)

    indexList = []

for index, row in haltestellen.iterrows(): 
    lat1 = row[1]
    lon1 = row[2]
    anzahlMeldungen= 0
    for i in range(len(meldungen['features'])): 
        coordinates = meldungen['features'][i]['geometry']['coordinates']
        #print(coordinates)
        lat2= coordinates[0]
        #print(lat2)
        lon2 = coordinates[1]
        if differenzZwischenZweiPunkten(lat1,lon1,lat2,lon2) < 100:
            anzahlMeldungen += 1
        i += 1
    indexList.append(anzahlMeldungen)
    print("bin dabei, index ", index, " row: ", row)

print(indexList)
