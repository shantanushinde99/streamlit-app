import streamlit as st
import numpy as np
import pickle as pk

# Load the model and scaler
loaded_model = pk.load(open("trained_model_lr.sav", "rb"))
scaled_data = pk.load(open("scaled_data.sav", "rb"))


# Function to convert the input values
def input_converter(inp):
    vcl = ['Two-seater', 'Minicompact', 'Compact', 'Subcompact', 'Mid-size', 'Full-size', 'SUV: Small', 'SUV: Standard', 'Minivan', 'Station wagon: Small', 'Station wagon: Mid-size', 'Pickup truck: Small', 'Special purpose vehicle', 'Pickup truck: Standard']
    trans = ['AV', 'AM', 'M', 'AS', 'A']
    fuel = ["D", "E", "X", "Z"]
    lst = []
    
    for i in range(6):
        if isinstance(inp[i], str):
            if inp[i] in vcl:
                lst.append(vcl.index(inp[i]))
            elif inp[i] in trans:
                lst.append(trans.index(inp[i]))
            elif inp[i] in fuel:
                if fuel.index(inp[i]) == 0:
                    lst.extend([1, 0, 0, 0])
                    break
                elif fuel.index(inp[i]) == 1:
                    lst.extend([0, 1, 0, 0])
                    break
                elif fuel.index(inp[i]) == 2:
                    lst.extend([0, 0, 1, 0])
                    break
                elif fuel.index(inp[i]) == 3:
                    lst.extend([0, 0, 0, 1])
        else:
            lst.append(inp[i])

    arr = np.asarray(lst).reshape(1, -1)
    arr = scaled_data.transform(arr)
    prediction = loaded_model.predict(arr)

    return round(prediction[0], 2)

# Streamlit app starts here
st.title('Fuel Consumption Prediction')

vehicle_classes = ['Two-seater', 'Minicompact', 'Compact', 'Subcompact', 'Mid-size', 'Full-size', 'SUV: Small', 'SUV: Standard', 'Minivan', 'Station wagon: Small', 'Station wagon: Mid-size', 'Pickup truck: Small', 'Special purpose vehicle', 'Pickup truck: Standard']
transmission_types = ['AV', 'AM', 'M', 'AS', 'A']
fuel_types = ["D", "E", "X", "Z"]

# User input
vehicle_class = st.selectbox("Vehicle Class", vehicle_classes)
engine_size = st.number_input("Engine Size (L)", min_value=0.0, format="%.1f")
cylinders = st.number_input("Cylinders", min_value=1, step=1)
transmission = st.selectbox("Transmission", transmission_types)
co2_rating = st.number_input("CO2 Rating", min_value=1, step=1)
fuel_type = st.selectbox("Fuel Type", fuel_types)

# Button to predict
if st.button('Predict'):
    result = input_converter([vehicle_class, engine_size, cylinders, transmission, co2_rating, fuel_type])
    st.success(f"Predicted Fuel Consumption: {result} L/100 km")

