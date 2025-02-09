import pickle
import pandas as pd
import streamlit as st
from datetime import datetime

# Load the trained model
model_path = r"C:\Users\DELL\Downloads\model.pkl"
try:
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)
except FileNotFoundError:
    st.error("Model file not found. Please ensure the file path is correct.")
    st.stop()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# Expected features
expected_columns = [
    'Total_Stops', 'Date', 'Month', 'Year', 'departure_hour', 'departure_min',
    'arrival_hour', 'arrival_min', 'duration_hour', 'duration_min',
    'Airline_Air Asia', 'Airline_Air India', 'Airline_GoAir', 'Airline_IndiGo',
    'Airline_Jet Airways', 'Airline_Jet Airways Business', 'Airline_Multiple carriers',
    'Airline_Multiple carriers Premium economy', 'Airline_SpiceJet', 'Airline_Trujet',
    'Airline_Vistara', 'Airline_Vistara Premium economy', 'Additional_Info_1 Long layover',
    'Additional_Info_1 Short layover', 'Additional_Info_2 Long layover', 'Additional_Info_Business class',
    'Additional_Info_Change airports', 'Additional_Info_In-flight meal not included',
    'Additional_Info_No Info', 'Additional_Info_No check-in baggage included',
    'Additional_Info_No info', 'Additional_Info_Red-eye flight', 'Source_Banglore',
    'Source_Chennai', 'Source_Delhi', 'Source_Kolkata', 'Source_Mumbai',
    'Destination_Banglore', 'Destination_Cochin', 'Destination_Delhi',
    'Destination_Hyderabad', 'Destination_Kolkata', 'Destination_New Delhi'
]

def predict_price(airline, additional_info, total_stops, source, destination, 
                 travel_date, departure_time, arrival_time, duration):
    try:
        departure_hour, departure_min = map(int, departure_time.split(':'))
        arrival_hour, arrival_min = map(int, arrival_time.split(':'))
    except Exception:
        raise ValueError("Invalid time format. Please use HH:MM format")
    
    date_day = travel_date.day
    month = travel_date.month
    year = travel_date.year
    duration_hour = int(duration)
    duration_min = int((duration - duration_hour) * 60)
    
    input_dict = {col: 0 for col in expected_columns}
    
    # Numeric features
    numeric_features = {
        'Total_Stops': total_stops,
        'Date': date_day, 'Month': month, 'Year': year,
        'departure_hour': departure_hour, 'departure_min': departure_min,
        'arrival_hour': arrival_hour, 'arrival_min': arrival_min,
        'duration_hour': duration_hour, 'duration_min': duration_min
    }
    input_dict.update(numeric_features)
    
    # Categorical features
    for col, value in [
        (f"Airline_{airline}", 1),
        (f"Additional_Info_{additional_info}", 1),
        (f"Source_{source}", 1),
        (f"Destination_{destination}", 1)
    ]:
        if col not in input_dict:
            raise ValueError(f"Invalid option: {col}")
        input_dict[col] = value
    
    input_df = pd.DataFrame([input_dict], columns=expected_columns)
    return model.predict(input_df)[0]

def set_css():
    st.markdown("""
        <style>
        .stApp {
            background: #0f0f0f;
            color: #ffffff;
            font-family: 'Arial', sans-serif;
        }
        .title {
            color: #00ff9d;
            font-size: 2.5rem;
            text-align: center;
            margin: 1rem 0;
            text-shadow: 0 0 10px #00ff9d;
        }
        .section {
            background: #1a1a1a;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
            border: 1px solid #333;
        }
        .stButton>button {
            background: #00ff9d;
            color: #000;
            font-weight: bold;
            border-radius: 25px;
            padding: 0.8rem 2rem;
            margin: 1rem auto;
            display: block;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            transform: scale(1.05);
            box-shadow: 0 0 15px #00ff9d;
        }
        .stSelectbox, .stDateInput, .stNumberInput {
            margin: 0.5rem 0;
        }
        .error {
            color: #ff4444;
            text-align: center;
            font-weight: bold;
        }
        .success {
            color: #00ff9d;
            font-size: 1.5rem;
            text-align: center;
            padding: 1rem;
            border: 2px solid #00ff9d;
            border-radius: 10px;
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Flight Price Predictor", page_icon="✈️", layout="centered")
    set_css()
    
    st.markdown('<h1 class="title">✈️ Flight Price Predictor</h1>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="section">', unsafe_allow_html=True)
        st.header("Flight Details")
        
        col1, col2 = st.columns(2)
        with col1:
            airline = st.selectbox("Airline", [
                "Air Asia", "Air India", "GoAir", "IndiGo", 
                "Jet Airways", "Jet Airways Business", "Multiple carriers",
                "Multiple carriers Premium economy", "SpiceJet", "Trujet",
                "Vistara", "Vistara Premium economy"
            ], help="Select your preferred airline")
            
            additional_info = st.selectbox("Additional Info", [
                "1 Long layover", "1 Short layover", "2 Long layover",
                "Business class", "Change airports", "In-flight meal not included",
                "No Info", "No check-in baggage included", "No info", "Red-eye flight"
            ])
            
            total_stops = st.number_input("Number of Stops", 0, 4, 0)

        with col2:
            source = st.selectbox("Departure City", 
                ["Banglore", "Chennai", "Delhi", "Kolkata", "Mumbai"])
            destination = st.selectbox("Arrival City", 
                ["Banglore", "Cochin", "Delhi", "Hyderabad", "Kolkata", "New Delhi"])
            
            if source == destination:
                st.markdown('<p class="error">Please select different cities for departure and arrival</p>', 
                          unsafe_allow_html=True)
                st.stop()

        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="section">', unsafe_allow_html=True)
        st.header("Timing Information")
        
        col1, col2 = st.columns(2)
        with col1:
            travel_date = st.date_input("Travel Date", datetime.today())
            departure_time = st.text_input("Departure Time (HH:MM)", "12:00")
        with col2:
            duration = st.number_input("Flight Duration (hours)", 0.5, 24.0, 2.0, 0.5)
            arrival_time = st.text_input("Arrival Time (HH:MM)", "14:00")
        
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Predict Flight Price"):
        try:
            price = predict_price(
                airline, additional_info, total_stops, source, destination,
                travel_date, departure_time, arrival_time, duration
            )
            st.markdown(f'<p class="success">Estimated Price: ₹{price:.2f}</p>', 
                      unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f'<p class="error">Error: {str(e)}</p>', 
                      unsafe_allow_html=True)

if __name__ == "__main__":
    main()