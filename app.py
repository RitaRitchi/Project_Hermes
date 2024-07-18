import requests
import json
from flask import Flask, render_template, jsonify

app = Flask(__name__)

api_key = ""

# Function to get real-time flight data from OpenSky Network API
def get_flight_data():
    url = "https://opensky-network.org/api/states/all"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Unable to fetch flight data (status code: {response.status_code})")
        return None

# Function to process and filter flight data
def process_flight_data(data):
    flights = []
    if data and 'states' in data:
        for flight in data['states']:
            if flight[5] and flight[6]:  # Ensure latitude and longitude are not None
                flights.append({
                    'icao24': flight[0],
                    'callsign': flight[1].strip(),
                    'origin_country': flight[2],
                    'latitude': flight[6],
                    'longitude': flight[5],
                    'altitude': flight[7],
                    'velocity': flight[9]
                })
    return flights

# Function to get real-time maritime data from MarineTraffic API
def get_vessel_data(api_key):
    url = f"http://services.marinetraffic.com/api/exportvesseltrack/v:2/{api_key}/timespan:10/protocol:jsono"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Unable to fetch vessel data (status code: {response.status_code})")
        return None

# Function to process and filter vessel data
def process_vessel_data(data):
    vessels = []
    if data:
        for vessel in data:
            vessels.append({
                'mmsi': vessel.get('MMSI'),
                'name': vessel.get('SHIPNAME'),
                'latitude': vessel.get('LAT'),
                'longitude': vessel.get('LON'),
                'speed': vessel.get('SPEED'),
                'course': vessel.get('COURSE'),
                'status': vessel.get('STATUS')
            })
    return vessels

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def flight_data():
    flight_data = get_flight_data()
    flights = process_flight_data(flight_data)
    
    vessel_data = get_vessel_data()
    vessels = process_vessel_data(vessel_data)
    
    return jsonify({'flights': flights, 'vessels': vessels})

@app.route('/data')
def marine_data():
    api_key = "YOUR_MARINETRAFFIC_API_KEY"
    vessel_data = get_vessel_data(api_key)
    vessels = process_vessel_data(vessel_data)
    
    return jsonify({'vessels': vessels})

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)
