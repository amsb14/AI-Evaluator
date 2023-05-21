# AI Evaluator Website

This is a web application that evaluates properties based on the given details from stakeholders. It predicts the price of the property and provides a summary report or evaluation for the property, comparing it with similar properties by calculating the average.

## Installation

To use this application, follow the instructions below:

1. Clone the repository using the provided link:
`git clone <repository_link>`

2. Install the required dependencies. Navigate to the project directory and run the following command:
pip install -r requirements.txt


3. Modify the `.env` file and add your own OpenAI key. You can obtain an OpenAI key by signing up on the OpenAI website.

4. Run the `app.py` file to start the web application:
python app.py


5. Open your preferred web browser and enter the following URL:
127.0.0.1:5000


## Usage

Once the web application is running, you can use it to evaluate properties. The following details are required from the stakeholders:

1. Category: Represents the property rating, ranging from 1 to 10, where 1 is the lowest and 10 is the highest.

2. Transaction Type: Select the transaction type from the available options (selling, renting).

3. Property Type: Choose the property type from the available options (villas, buildings, flats, lands).

4. City: Select the city from the available options. The application supports all cities in Saudi Arabia.

5. District: Choose the district from the available options. The application supports all districts within each city.

6. Number of Bedrooms: Enter the number of bedrooms in the property.

7. Number of Living Rooms: Enter the number of living rooms in the property.

8. Number of Bathrooms: Enter the number of bathrooms in the property.

9. Area in sq.m: Specify the area of the property in square meters.

10. Street Width: Enter the width of the street where the property is located.

11. Direction: Specify the direction of the property.

After entering all the required details, click the "Evaluate" or "Submit" button. The web application will process the information and provide the following outputs:

- Predicted Price: The estimated price of the property based on the given details.

- Summary Report: An evaluation of the property, including a comparison with similar properties by calculating the average.

Please note that the accuracy of the predicted price and evaluation may vary, as they are based on AI models and historical data.

Feel free to explore the web application and evaluate various properties based on different input combinations.

## License
