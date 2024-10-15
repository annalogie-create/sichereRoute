import requests
import json

def fetch_osm_data(lat, lon, radius=20):
    # Define the Overpass API endpoint
    overpass_url = "http://overpass-api.de/api/interpreter"
    
    # Define the Overpass QL query
    overpass_query = f"""
    [out:json];
    (
      node(around:{radius},{lat},{lon})["leisure"="park"];
      node(around:{radius},{lat},{lon})["natural"="wood"];
      way(around:{radius},{lat},{lon})["leisure"="park"];
      way(around:{radius},{lat},{lon})["landuse"="grass"];
      way(around:{radius},{lat},{lon})["natural"="wood"];
    );
    out body;
    """
    
    # Send the request to the Overpass API
    response = requests.post(overpass_url, data=overpass_query)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        print(data)
        return data
    else:
        print("Error:", response.status_code)
        return None

# Beispielkoordinate (Hamburg)
latitude = 54.015547
longitude = 10.017094

fetch_osm_data(latitude, longitude)