# Flight-Price-Prediction-Project

This project focuses on predicting flight prices using a dataset containing various features such as airline, source, destination, departure time, arrival time, duration, total stops, and additional information. The goal is to build a machine learning model that can accurately predict flight prices based on these features.

Dataset Overview
The dataset contains the following columns:

Airline: The airline company.

Date_of_Journey: The date of the flight.

Source: The departure city.

Destination: The arrival city.

Route: The route taken by the flight.

Dep_Time: The departure time.

Arrival_Time: The arrival time.

Duration: The duration of the flight.

Total_Stops: The number of stops in the flight.

Additional_Info: Additional information about the flight.

Price: The target variable, representing the price of the flight.

Data Preprocessing
The dataset was preprocessed to handle missing values, convert categorical variables into numerical ones using one-hot encoding, and extract useful features such as:

Date, Month, and Year extracted from the Date_of_Journey.

Departure Hour and Departure Minute extracted from the Dep_Time.

Arrival Hour and Arrival Minute extracted from the Arrival_Time.

Duration Hour and Duration Minute extracted from the Duration.

Model Building
A Random Forest Regressor was used to predict flight prices. The model was trained on 80% of the dataset and tested on the remaining 20%. The model's performance was evaluated using the following metrics:

Mean Absolute Error (MAE): 920.79

Mean Squared Error (MSE): 3,319,622.32

R-squared (R²): 0.8431

Feature Importance
The top 5 most important features for predicting flight prices are:

Duration Hour (0.456)

Date (0.087)

Additional_Info_In-flight meal not included (0.082)

Airline_Jet Airways Business (0.070)

Airline_Jet Airways (0.068)

Model Deployment
The trained model was saved using Pickle for future use and deployment. The model can be loaded and used to predict flight prices based on new input data.

How to Use
Clone the repository.

Install the required dependencies (e.g., pandas, scikit-learn, numpy).

Run the Jupyter notebook to train the model or load the pre-trained model using model.pkl.

Use the model to predict flight prices by providing the necessary input features.

Dependencies
Python 3.x

pandas

numpy

scikit-learn

pickle

