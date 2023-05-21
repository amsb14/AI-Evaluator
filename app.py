import openai
from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import joblib

import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
loaded_model = joblib.load('GaiaPropertyPredictor2.pkl')

df = pd.read_csv("before_enc_features.csv")
districts = df['district'].tolist()
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

def GPT_prompt(predicted_price, mean_price, category, transactionType,  propertyType, city, district, bedrooms, livings, wc, area, streetWidth, streetDirection):
    prompt = f"""
You help stakeholders in real estate by evaluating properties (assessing the value, conditions, and potential of a property through thorough analysis and comparison to determine its worth). Stakeholders use a website that leverages ML model which predicts the price of a property based on certain criteria.

The website asks the user for these properties:
1- Category (represents property rating ranging from 1 to 10 where 1 is lowest and 10 highest)
2- Transaction Type (has 2 types: selling, renting)
3- Property Type (has 4 types: villas, buildings, flats, lands)
4- City (all the cities in Saudi Arabia)
5- District (all in the districts in each city)
6- Number of bedrooms (number of bedrooms in the property)
7- Number of living rooms (number of living rooms in the property)
8- Number of bathrooms (number of bathrooms in the property)
9- Area in sq.m (the area in square meters)
10- Street width
11- Direction direction


Now the user has entered the following details: {category}, {transactionType},  {propertyType}, {city}, {district}, {bedrooms}, {livings}, {wc}, {area}, {streetWidth}, {streetDirection}.

The predicted price for this property outputted by the model was: {predicted_price}
The average price for a number of properties with similar details was: {mean_price}

Your task is to create a report explaining to the stakeholder that the predicted price is high, moderate, or low based on if the predicted price is equal or less than the mean price or higher than the mean without being biased.
If the mean does not exist or is not applicable, inform the stakeholder that there are no many prices for such property details at the moment.

Also, you can say if the predicted price is above average, indicating the property may possess certain exceptional features, and location advantages such as government departments, schools, banks, mosques, hospitals, and parks.

DONT use welcome or conclusion words or repeat the above details.

Make sure the whole report DOES NOT  EXCEED 300 WORDS! BUT not less than 250 WORDS.

    """

    return prompt

def generate_text(predicted_price, mean_price, category, transactionType, propertyType, city, district, bedrooms, livings, wc, area,
                                   streetWidth, streetDirection):
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=GPT_prompt(predicted_price, mean_price, category, transactionType, propertyType, city, district, bedrooms, livings, wc, area,
                                   streetWidth, streetDirection),
      temperature=0.75,
      max_tokens=300,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )
    response = response['choices'][0]['text']

    print(GPT_prompt(predicted_price, mean_price, category, transactionType, propertyType, city, district, bedrooms, livings, wc, area,
                                   streetWidth, streetDirection))

    return response

# Create a dictionary with cities as keys and lists of districts as values
from collections import defaultdict
city_districts = defaultdict(list)
for index, row in df.iterrows():
    city_districts[row['city']].append(row['district'])

# Remove duplicates by converting lists to sets and then back to lists
for city, districts in city_districts.items():
    city_districts[city] = list(set(districts))

# Convert the default dict back to a regular dict
city_districts = dict(city_districts)

# --------------------
app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        category = request.form.get('category')
        transactionType = request.form.get('transaction')
        propertyType = request.form.get('property')
        city = request.form.get('city')
        district = request.form.get('district')
        bedrooms = request.form.get('bedrooms')
        livings = request.form.get('livings')
        wc = request.form.get('wc')
        area = request.form.get('area')
        streetWidth = request.form.get('streetWidth')
        streetDirection = request.form.get('streetDirection')


        print(category, transactionType, propertyType, city, district, bedrooms, livings, wc, area, streetWidth,
              streetDirection)

        predicted_price = new_data(category, transactionType, propertyType, city, district, bedrooms, livings, wc, area,
                                   streetWidth, streetDirection)
        print("Prediction:", predicted_price)

        mean_price = mean_value(city, district, propertyType, transactionType, area)
        print('The mean price', mean_price)

        summary_text = generate_text(predicted_price, mean_price, category, transactionType, propertyType, city, district, bedrooms, livings, wc, area,
                                   streetWidth, streetDirection)
        predicted_price_sar = f"{predicted_price} SAR"
        print("Summary:", summary_text)


        return render_template('HOME4.html', city_districts=city_districts, category=category,
                               transactionType=transactionType, propertyType=propertyType, city=city, district=district,
                               bedrooms=bedrooms, livings=livings, wc=wc, area=area, streetWidth=streetWidth,
                               streetDirection=streetDirection, predicted_price=predicted_price_sar, summary_text=summary_text)
    return render_template('HOME4.html', city_districts=city_districts)



if __name__ == "__main__":
    app.run(debug=True, port=5000)
