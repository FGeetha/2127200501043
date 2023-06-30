from flask import Flask, jsonify
import requests
import datetime
import functools

app = Flask(__name__)

API_URL = "https://api.johndoerailways.com"
AUTH_TOKEN = "your-auth-token"  # Replace with your authentication token

def get_train_data():
    response = requests.get(f"{API_URL}/trains", headers={"Authorization": AUTH_TOKEN})
    return response.json()["trains"]

@functools.lru_cache(maxsize=128)  # Caching decorator
def get_seat_availability(train_id):
    response = requests.get(f"{API_URL}/seat_availability/{train_id}", headers={"Authorization": AUTH_TOKEN})
    return response.json()["seats"]

@functools.lru_cache(maxsize=128)  # Caching decorator
def get_train_prices(train_id):
    response = requests.get(f"{API_URL}/prices/{train_id}", headers={"Authorization": AUTH_TOKEN})
    return response.json()["prices"]

@app.route("/trains", methods=["GET"])
def get_train_schedules():
    current_time = datetime.datetime.now()
    end_time = current_time + datetime.timedelta(hours=12)
    
    trains = get_train_data()
    
    train_schedules = []
    
    for train in trains:
        departure_time = datetime.datetime.strptime(train["departure_time"], "%Y-%m-%d %H:%M:%S")
        
        if current_time < departure_time < end_time:
            seats = get_seat_availability(train["train_id"])
            prices = get_train_prices(train["train_id"])
            
            train_schedule = {
                "train_id": train["train_id"],
                "departure_time": train["departure_time"],
                "seats": seats,
                "prices": prices
            }
            
            train_schedules.append(train_schedule)
    
    sorted_trains = sorted(train_schedules, key=lambda t: (min(t["prices"].values()), -sum(t["seats"].values()), -datetime.datetime.strptime(t["departure_time"], "%Y-%m-%d %H:%M:%S").timestamp()))
    
    return jsonify(sorted_trains)

if __name__ == "__main__":
    app.run()
