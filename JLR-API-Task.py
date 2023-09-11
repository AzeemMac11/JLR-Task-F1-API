#!/usr/bin/env python
# coding: utf-8


#import requests
from pip._vendor import requests
import xml.etree.ElementTree as ET
import json


# Define API URL for the 2023 F1 season based on constructors' standings
api_url = "http://ergast.com/api/f1/2023/constructorStandings.json"


# Fetch data from API
response = requests.get(api_url)
data = response.json()


# Initialize a dictionary to store the best circuit for each constructor
best_circuits = {}


season = data["MRData"]["StandingsTable"]["StandingsLists"][0]["season"]


# Iterate through the constructor standings data
for constructor in data["MRData"]["StandingsTable"]["StandingsLists"][0]["ConstructorStandings"]:
    constructor_id = constructor["Constructor"]["constructorId"]
    constructor_name = constructor["Constructor"]["name"]
    # season = constructor["season"]
    
    # Define API URL to fetch the race results for this constructor in all seasons
    api_url2 = f"http://ergast.com/api/f1/constructors/{constructor_id}/results.json"
    
    # Fetch data for all seasons
    response2 = requests.get(api_url2)
    data2 = response2.json()

    # Initialize variables to track the best circuit and points
    best_circuit = None
    best_points = 0

    # Iterate through race results for this constructor
    for race in data2["MRData"]["RaceTable"]["Races"]:
      race_name = race["raceName"]
      points = int(float(race["Results"][0]["points"]))
        
    # Check if this race had more points than the current best
    if points > best_points:
      best_points = points
      best_circuit = race_name
    
        
    # Store the best circuit for this constructor
    best_circuits[constructor_name] = {
        "constructor_name": constructor_name,
        "constructor_id": constructor_id,
        "best_circuit": best_circuit,
        "season": season,
    }
    

# Results in XML format
root = ET.Element("ConstructorBestCircuits")
for constructor_name, info in best_circuits.items():
    constructor_elem = ET.SubElement(root, "Constructor")
    ET.SubElement(constructor_elem, "Name").text = constructor_name
    ET.SubElement(constructor_elem, "ConstructorID").text = info["constructor_id"]
    ET.SubElement(constructor_elem, "BestCircuit").text = info["best_circuit"]
    ET.SubElement(constructor_elem, "Season").text = info["season"]


xml_result = ET.tostring(root, encoding="unicode")


# Print the results
print("XML Output:")
print(xml_result)


# Results in JSON format
json_result = json.dumps(best_circuits, indent=4)


print("\nJSON Output:")
print(json_result)


# Save the results to files if needed
# with open("constructor_best_circuits.xml", "w") as xml_file:
# xml_file.write(xml_result)

# with open("constructor_best_circuits.json", "w") as json_file:
# json_file.write(json_result)

