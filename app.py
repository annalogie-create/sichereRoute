import pandas as pd
import json
import math
import requests

def fetch_osm_data(lat, lon, radius):
    # Define the Overpass API endpoint
    overpass_url = "http://overpass-api.de/api/interpreter"
    
# Define the Overpass QL query
    overpass_query = f"""
    [out:json];
    (
      node(around:{radius},{lat},{lon})["leisure"="park"];
      node(around:{radius},{lat},{lon})["natural"="wood"];
      node(around:{radius},{lat},{lon})["natural"="scrub"];
      way(around:{radius},{lat},{lon})["leisure"="park"];
      way(around:{radius},{lat},{lon})["natural"="wood"];
      way(around:{radius},{lat},{lon})["natural"="scrub"];
    );
    out body;
    """

    #way(around:{radius},{lat},{lon})["landuse"="grass"];
    
    # Send the request to the Overpass API
    response = requests.post(overpass_url, data=overpass_query)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        if(data['elements']):
            print(len(data['elements']))
            return len(data['elements'])
        return 0
    else:
        print("Error:", response.status_code)
        return 0

filter = [
    "Straßenbeleuchtung ausgefallen",
    "Gewässerverunreinigung",
    "Beschädigte Brücke, Tunnel, Mauer, Treppe",
    "Beschädigtes Verkehrszeichen",
    "Ampel gestört",
    "Straßenbeleuchtung gestört",
    "Beschädigter Stromkasten",
    "Verunreinigung und Vandalismus",
    "Beschädigte Geländer, Poller, Fahrradständer, Sitzgelegenheit",
]

def inFilter(feature):
    return feature["properties"]["skat_text"] in filter

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

def printCompleteData(indexList):
    sicherheitsIndex = []
    for index, row in haltestellen.iterrows():
        sicherheitsIndex.append({"name": row[0], "latitude": row[1], "longitude": row[2], "count": indexList[index]})
    print(json.JSONEncoder().encode(sicherheitsIndex))

def getAnzahlMeldungen(haltestelleLat, haltestelleLon):
    anzahlMeldungen= 0
    for i in range(len(meldungen['features'])): 
        coordinates = meldungen['features'][i]['geometry']['coordinates']
        #print(coordinates)
        lat2= coordinates[0]
        #print(lat2)
        lon2 = coordinates[1]
        if differenzZwischenZweiPunkten(haltestelleLat,haltestelleLon,lat2,lon2) < 100:
            anzahlMeldungen += 1
        i += 1
    return anzahlMeldungen
    #print("bin dabei, index ", index, " row: ", row)

haltestellen = pd.read_excel("data/HVV-Haltestellen.xlsx", header = 0)
with open("data/anliegen_extern.json", 'r', encoding='utf-8') as datei:
    meldungen = json.load(datei)
    features = [feature for feature in meldungen['features'] if inFilter(feature)]
    indexList = []

for index, row in haltestellen.iterrows(): 
    lat = row[2]
    lon = row[1]
    print("haltestelle: ",row[0]," lat: ", lat, ", lon: ", lon)
    anzahlMeldungen = getAnzahlMeldungen(lat, lon)
    numberOfGruenflaechen = fetch_osm_data(lat, lon, 10)
    indexList.append(anzahlMeldungen)
    
# print(indexList)
printCompleteData(indexList)