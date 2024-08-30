from flask import Flask, render_template, jsonify
import os, re

app = Flask(__name__)

def fetch_cpu_temp():
	out = os.popen("vcgencmd measure_temp").readline()
	temperature = re.sub('[^0-9.]', '', out)
	# print (f"Current temperature is: {temperature} ºC")
	return temperature

@app.route("/")
def home():
	cpu_temperature = float(fetch_cpu_temp())
	return render_template("home.html" , cpu_temp = cpu_temperature)

@app.route('/temperature')
def temperature():
	temp =  fetch_cpu_temp()
	return jsonify(temperature=temp)

if __name__ == "__main__":
	app.run(host = "0.0.0.0", port = 8000)
