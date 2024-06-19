import requests
from flask import Flask, render_template, jsonify

app = Flask(__name__)

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

# Placeholder function to get real-time maritime data
def get_vessel_data():
    # For real implementation, use a proper maritime API like MarineTraffic with a valid API key
    # url = "https://example-maritime-api.com/vessel-data"  # Replace with actual maritime API URL
    # response = requests.get(url)
    
    # Sample data for illustration purposes
    data = [
        {'MMSI': '123456789', 'SHIPNAME': 'Sample Vessel 1', 'LAT': 37.7749, 'LON': -122.4194, 'SPEED': 14, 'COURSE': 180, 'STATUS': 'Underway'},
        {'MMSI': '987654321', 'SHIPNAME': 'Sample Vessel 2', 'LAT': 40.7128, 'LON': -74.0060, 'SPEED': 10, 'COURSE': 90, 'STATUS': 'At Anchor'}
    ]
    return data

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
def data():
    flight_data = get_flight_data()
    flights = process_flight_data(flight_data)
    
    vessel_data = get_vessel_data()
    vessels = process_vessel_data(vessel_data)
    
    return jsonify({'flights': flights, 'vessels': vessels})

if __name__ == '__main__':
    app.run(debug=True)
