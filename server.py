# Flask instance which running our server
from flask import Flask, render_template, request
from weather import get_current_weather
from waitress import serve

app = Flask(__name__) # Setting up WSGI app

@app.route('/')
@app.route('/index') 
def index():
    return render_template('index.html')

@app.route('/weather')
def get_weather():
    city = request.args.get('city') # We get this info from link body
    if not bool(city.strip()): # Works if input line was empty
        city = "Minsk"
    weather_data = get_current_weather(city)
    
    # City is not found by API
    if not weather_data['cod'] == 200:
        return render_template("city-not-found.html")


    return render_template( # Returns HTML file with params substitution
        "weather.html",
        title = weather_data["name"],
        status = weather_data["weather"][0]["description"].capitalize(),
        temp=f"{weather_data['main']['temp']:.1f}",
        feels_like = f"{weather_data['main']['feels_like']:.1f}"
    )



if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=8000, debug=True) # Flask Development server (instead of waitress)
    serve(app, host = "0.0.0.0", port=8000) # Running WSGI server

