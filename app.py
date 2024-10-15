import pandas as pd
import json
import math
import numpy as np

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



def printCompleteData(indexList, haltestellen):
    haltestellenMitSicherheitsindex = haltestellen
    haltestellenMitSicherheitsindex['index'] = indexList
    haltestellenMitSicherheitsindex.to_csv('out.csv')

def min_max_normalization(data):
    """
    Perform min-max normalization on the given data.
    
    Parameters:
    data (list or np.ndarray): The input data to be normalized.
    
    Returns:
    np.ndarray: Normalized data in the range [0, 1].
    """
    data = np.array(data)
    min_val = np.min(data)
    max_val = np.max(data)
    
    # Avoid division by zero
    if max_val - min_val == 0:
        return np.zeros_like(data)  # or return data directly if you prefer

    normalized_data = (data - min_val) / (max_val - min_val)
    return normalized_data



haltestellen = pd.read_excel("data/HVV-Haltestellen.xlsx", header = 0)


with open("data/anliegen_extern.json", 'r', encoding='utf-8') as datei:
    meldungen = json.load(datei)
    features = [feature for feature in meldungen['features'] if inFilter(feature)]
    indexList = []

for index, row in haltestellen.iterrows(): 
    lat1 = row[1]
    lon1 = row[2]
    anzahlMeldungen= 0
    for i in range(len(features)): 
        coordinates = meldungen['features'][i]['geometry']['coordinates']
        #print(coordinates)
        lat2= coordinates[0]
        #print(lat2)
        lon2 = coordinates[1]
        if differenzZwischenZweiPunkten(lat1,lon1,lat2,lon2) < 100:
            anzahlMeldungen += 1
        i += 1
    indexList.append(anzahlMeldungen)
    print("durchlaufe Haltestellen - index: ", index, " row: ", row[0])

normalizedIndexList = min_max_normalization(indexList)

printCompleteData(normalizedIndexList, haltestellen)
