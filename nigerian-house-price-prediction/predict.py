import pickle
import pandas as pd
import numpy as np

X_data = pd.read_csv("dataset\X_data.csv")
expected_columns = X_data.columns.tolist()

title_rankings = {
    'Detached Duplex': 1,
    'Semi Detached Duplex': 2,
    'Terraced Duplexes': 3,
    'Detached Bungalow': 4,
    'Semi Detached Bungalow': 5,
    'Block of Flats': 6,
    'Terraced Bungalow': 7
}

def predict(bedrooms, bathrooms, toilets, parking_space, title, state, town):
    user_data = pd.DataFrame(0, index=[0], columns=expected_columns)
    user_data["bedrooms"] = bedrooms
    user_data["bathrooms"] = bathrooms
    user_data["toilets"] = toilets
    user_data["parking_space"] = parking_space
    user_data["title_rank"] = title_rankings[title]
    state_column_name = f'state_{str(state).lower() + str(town).lower()}'
    if state_column_name in expected_columns:
        user_data[state_column_name] = 1
    with open('models/ridge_reg.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    print(user_data)
    predicted_price = model.predict(user_data)
    # print("Predicted Price:", int(np.exp(np.exp(predicted_price[0]))))
    return int(np.exp(np.exp(predicted_price[0])))