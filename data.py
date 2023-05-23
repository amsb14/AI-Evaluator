import pandas as pd
import numpy as np
from collections import defaultdict, OrderedDict
from model import loaded_model


df = pd.read_csv("before_enc_features.csv")

def get_city_code(user_input, encoded_feature, feature):
    # Filter the DataFrame based on user input
    filtered_df = df[df[feature] == user_input]

    if len(filtered_df) > 0:
        # Retrieve the corresponding value from 'city_encoded' column
        city_code = filtered_df[encoded_feature].values[0]
        return city_code
    else:
        return None


def new_data(category, transaction_type, property_type, city, district, beds, livings, wc, area, street_width, street_direction):
    new_data = pd.DataFrame({
        'category': [float(category)],
        'beds': [float(beds)],
        'livings': [float(livings)],
        'wc': [float(wc)],
        'area': [float(area)],
        'street_width': [float(street_width)],
        'street_direction': [float(street_direction)],
        'city': [get_city_code(city, 'en_city', 'city')],
        'district': [get_city_code(district, 'en_district', 'district')],
        'transaction_type': [1 if transaction_type == 'Rent' else 0],
        'villas': [1 if property_type == 'villa' else 0],
        'buildings': [1 if property_type == 'building' else 0],
        'flats': [1 if property_type == 'flat' else 0],
        'lands': [1 if property_type == 'land' else 0],
    })

    reshaped_array = np.array(new_data).reshape(1, -1)
    y_pred = loaded_model.predict(reshaped_array)

    return int(y_pred[0])


def filter_properties(city, district, property_type, transaction_type, user_area):

    df = pd.read_csv("Cleaned_Riyadh_Without_Lng_Lat.csv")
    if property_type not in ['villas', 'buildings', 'lands', 'flats']:
        raise ValueError("Invalid property_type. Valid options are: 'villas', 'buildings', 'lands', 'flats'.")

    # Calculate the 10% range for the area
    user_area = float(user_area)
    # print("#######################", user_area)
    area_lower_bound = user_area * 0.9
    area_upper_bound = user_area * 1.1

    # Filter the DataFrame
    print("####################", property_type)
    filtered_df = df[(df['city'] == city) &
                     (df['district'] == district) &
                     (df[property_type] == 1) &
                     (df['transaction_type'] == transaction_type) &
                     (df['area'] >= area_lower_bound) &
                     (df['area'] <= area_upper_bound)]

    return filtered_df[['city', 'district', property_type, 'transaction_type', 'price', 'area']]


def mean_value(user_city, user_district, user_property_type, user_transaction_type, user_area):
    filtered_df = filter_properties(user_city, user_district, user_property_type, user_transaction_type, user_area)
    property_mean_prices = filtered_df['price'].mean()

    if pd.isna(property_mean_prices):
        return "Not Applicable"

    return int(property_mean_prices)

# districts = df['district'].tolist()

# Create a dictionary with cities as keys and lists of districts as values
city_districts = defaultdict(set)
for index, row in df.iterrows():
    city_districts[row['city']].add(row['district'])

ordered_city_districts = OrderedDict(sorted(city_districts.items()))

# Convert the ordered dictionary back to a regular dictionary
city_districts = {city: sorted(districts) for city, districts in ordered_city_districts.items()}
