import requests
import json

def fetch_osm_data(lat, lon, radius=100):
    print("Start")
    # Define the Overpass API endpoint
    overpass_url = "http://overpass-api.de/api/interpreter"
    
    # Define the Overpass QL query
    overpass_query = f"""
    [out:json];
    (
      node(around:{radius},{lat},{lon})["leisure"="park"];
    );
    out body;
    """
    
    # Send the request to the Overpass API
    response = requests.post(overpass_url, data=overpass_query)
    print("response: ", response)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        print(data)
        return data
    else:
        print("Error:", response.status_code)
        return None

# Beispielkoordinate (Hamburg)
latitude = 53.5511
longitude = 9.9937

fetch_osm_data(latitude, longitude, 10000)
