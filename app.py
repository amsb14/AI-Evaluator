from flask import Flask, render_template, request
from data import new_data, mean_value, city_districts

from gpt_generator import generate_text

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
