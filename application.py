
import joblib
import os
import numpy as np
import pandas as pd
from config.paths_config import MODEL_OUTPUT_PATH
from flask import Flask, render_template, request

app = Flask(__name__)

# Load the trained model
loaded_model = joblib.load(MODEL_OUTPUT_PATH)

# Mappings
market_segment_map = {
    "Aviation": 0,
    "Complimentary": 1,
    "Corporate": 2,
    "Offline": 3,
    "Online": 4
}

meal_plan_map = {
    "Meal Plan 1": 1,
    "Meal Plan 2": 2,
    "Meal Plan 3": 3,
    "Not Selected": 0
}

room_type_map = {
    "Room Type 1": 1,
    "Room Type 2": 2,
    "Room Type 3": 3,
    "Room Type 4": 4,
    "Room Type 5": 5,
    "Room Type 6": 6,
    "Room Type 7": 7
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Get values from the form
            lead_time = int(request.form["lead_time"])
            no_of_special_request = int(request.form["no_of_special_request"])
            avg_price_per_room = float(request.form["avg_price_per_room"])
            arrival_month = int(request.form["arrival_month"])
            arrival_date = int(request.form["arrival_date"])

            # Convert categorical strings to integers
            market_segment_type = market_segment_map[request.form["market_segment_type"]]
            type_of_meal_plan = meal_plan_map[request.form["type_of_meal_plan"]]
            room_type_reserved = room_type_map[request.form["room_type_reserved"]]

            no_of_week_nights = int(request.form["no_of_week_nights"])
            no_of_weekend_nights = int(request.form["no_of_weekend_nights"])

            # Create DataFrame
            columns = [
                "lead_time", "no_of_special_request", "avg_price_per_room",
                "arrival_month", "arrival_date", "market_segment_type",
                "no_of_week_nights", "no_of_weekend_nights",
                "type_of_meal_plan", "room_type_reserved"
            ]
            values = [[
                lead_time, no_of_special_request, avg_price_per_room,
                arrival_month, arrival_date, market_segment_type,
                no_of_week_nights, no_of_weekend_nights,
                type_of_meal_plan, room_type_reserved
            ]]
            features = pd.DataFrame(values, columns=columns)

            # Predict
            prediction = loaded_model.predict(features)
            result = "The Customer is not going to cancel the reservation✅" if prediction[0] == 1 else "Customer will Cancel the Reservation❌"

            return render_template('index.html', prediction=result)

        except Exception as e:
            return render_template('index.html', prediction=f"Error: {str(e)}")

    return render_template('index.html', prediction=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
