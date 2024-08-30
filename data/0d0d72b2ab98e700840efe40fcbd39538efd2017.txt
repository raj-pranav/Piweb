from flask import Flask, render_template, jsonify
import os, re, time

app = Flask(__name__)


@app.route("/")
def home():
	cpu_temp = fetch_cpu_temp()
	return render_template("home.html" , cpu_temp = cpu_temp)

def fetch_cpu_temp():
	out = os.popen("vcgencmd measure_temp").readline()
	curr_temp = re.sub('[^0-9.]', '', out)
	# print (f"Current temperature is: {curr_temp} ºC")
	return curr_temp

@app.route('/temperature')
def temperature():
	temp =  fetch_cpu_temp()
	return jsonify(temperature=temp)

if __name__ == "__main__":
	app.run(host = "0.0.0.0", port = 8000)
