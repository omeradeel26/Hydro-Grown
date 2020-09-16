from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/temperature', methods=['POST'])
def temperature():
    precip = []
    solar = []
    temp_c = []

    K = { 'roses': 0.8,
          'sunflowers': 0.71,
          'corn': 0.725,
          'carrots': 1.0
         }

    cityname = request.form['city']
    statename = request.form['state']
    hours = int(request.form['hour'])
    complete_url = 'https://api.weatherbit.io/v2.0/forecast/hourly?city=' + cityname + ',' +statename + '&key=4149057ddc474d98ad7cc65109d32e09&hours=' + str(hours)
    r = requests.get(complete_url)
    json_object = r.json()


    for i in range(hours):
         precip.append(json_object['data'][i]['precip'])
         solar.append(json_object['data'][i]['solar_rad'])
         temp_c.append(json_object['data'][i]['temp'])

    precip = int(round(sum(precip)/len(precip),2))
    solar = int(round(sum(solar)/len(solar),2))
    temp_c = int(round(sum(temp_c)/len(temp_c),2))

    Temp = temp_c #Mean Temp Celsius
    Precipitation = precip #mm per square meter
    K = 1.01
    Solar_Radiation = solar 
    Solar_Radiation = (Solar_Radiation * (60*60*24))/1000000 #MegaJoules / day

    last_time_watered = 0
    time_to_water = 24 #military standard time 
    hours_since_watered = time_to_water - last_time_watered

    ETR = 0.0135 * (Temp+17.78) * Solar_Radiation * (238.8/(595.5-(0.55*Temp)))
    ET = K * ETR
    Amount_to_water_perhour = (ET - Precipitation)/24
    Total_amount_to_water = str(round(Amount_to_water_perhour * hours_since_watered,2))

    return render_template('temperature.html', total=Total_amount_to_water, city=cityname,state=statename, h =hours)

@app.route('/')
def landingpage():
    return render_template('landingpage.html')
    
@app.route('/loginpage')
def login():
    return render_template('login.html')

@app.route('/index')
def index():
    return render_template('index.html')

if  __name__ == '__main__':
    app.run(debug=True)