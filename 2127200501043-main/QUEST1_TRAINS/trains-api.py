from flask import Flask, jsonify
import requests
import datetime
import functools

app = Flask(__name__)

API_URL = "https://api.johndoerailways.com"
AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODgxMzk5MDQsImNvbXBhbnlOYW1lIjoiRXhwcmVzcyBUcmFpbnMgIiwiY2xpZW50SUQiOiI0ZmZjM2NmYy04ZTI2LTQzMWQtOTA2ZC05ZmI2YTJmMDRhMmUiLCJvd25lck5hbWUiOiIiLCJvd25lckVtYWlsIjoiIiwicm9sbE5vIjoiNDMifQ.1Bdy--VDhW2UjZOydjhdDXZLa4wX15iXNUzLZKXVb5Y"  # Replace with your authentication token

def get_train_data():
    response = requests.get(f"{API_URL}/trains", headers={"Authorization": AUTH_TOKEN})
    return response.json()["trains"]

@functools.lru_cache(maxsize=128)  # Caching decorator
def get_seat_availability(trainNumber):
    response = requests.get(f"{API_URL}/seat_availability/{trainNumber}", headers={"Authorization": AUTH_TOKEN})
    return response.json()["seatsAvailable"]

@functools.lru_cache(maxsize=128)  # Caching decorator
def get_train_prices(train_id):
    response = requests.get(f"{API_URL}/price/{trainNumber}", headers={"Authorization": AUTH_TOKEN})
    return response.json()["price"]

@app.route("/trains", methods=["GET"])
def get_train_schedules():
    current_time = datetime.datetime.now()
    end_time = current_time + datetime.timedelta(hours=12)
    
    trains = get_train_data()
    
    train_schedules = []
    
    for train in trains:
        departure_time = datetime.datetime.strptime(train["departureTime"], "%Y-%m-%d %H:%M:%S")
        
        if current_time < departure_time < end_time:
            seats = get_seat_availability(train["trainNumber"])
            prices = get_train_prices(train["trainNumber"])
            
            train_schedule = {
                "trainNumber": train["trainNumber"],
                "departureTime": train["departureTime"],
                "seatAvailable": seats,
                "price": prices
            }
            
            train_schedules.append(train_schedule)
    
    sorted_trains = sorted(train_schedules, key=lambda t: (min(t["price"].values()), -sum(t["seats"].values()), -datetime.datetime.strptime(t["departureTime"], "%Y-%m-%d %H:%M:%S").timestamp()))
    
    return jsonify(sorted_trains)

if __name__ == "__main__":
    app.run()
    