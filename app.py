from flask import Flask, render_template, jsonify
import os, re, sqlite3
from datetime import datetime

app = Flask(__name__)

def fetch_cpu_temp():
	out = os.popen("vcgencmd measure_temp").readline()
	temperature = re.sub('[^0-9.]', '', out)
	# print (f"Current temperature is: {temperature} ºC")
	return temperature

def store_temperature(temp):
	conn = sqlite3.connect('temperature.db')
	c = conn.cursor()
	c.execute('''CREATE TABLE IF NOT EXISTS temperatures
                 (id INTEGER PRIMARY KEY, timestamp TEXT, temp REAL)''')
	c.execute("INSERT INTO temperatures (temp, timestamp) VALUES (?, ?)", (datetime.now() , temp))

	conn.commit()
	conn.close()


@app.route("/")
def home():
	# cpu_temperature = float(fetch_cpu_temp())
	return render_template("home.html") # , cpu_temp = cpu_temperature)

@app.route('/temperature')
def temperature():
	cpu_temperature =  fetch_cpu_temp()
	store_temperature(cpu_temperature)  # Store temperature in DB
	return jsonify(temperature=cpu_temperature)


if __name__ == "__main__":
	app.run(host = "0.0.0.0", port = 8000)
