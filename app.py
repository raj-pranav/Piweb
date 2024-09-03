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
	c.execute("INSERT INTO temperatures (timestamp, temp) VALUES (?, ?)", (datetime.now(), temp ))

	conn.commit()
	conn.close()

def temperature_stats(): # for updating table values in web
    conn = sqlite3.connect('temperature.db')
    c = conn.cursor()
    c.execute("SELECT MAX(temp), MIN(temp), AVG(temp) FROM temperatures")
    high, low, avg = c.fetchone()
    conn.close()
    return high, low, round(avg,1)

def temperature_history():
	""" Output temperature history stored in the DB  """
	conn = sqlite3.connect('temperature.db')
	c = conn.cursor()
	c.execute("SELECT * FROM temperatures ORDER BY timestamp DESC LIMIT 40 ")
	data = c.fetchall()
	conn.close()
	# Convert data to a format suitable for Chart.js
	labels = [row[1] for row in data]
	values = [row[2] for row in data]
	print (labels, values)
	return labels, values


@app.route("/")
def home():
	# cpu_temperature = float(fetch_cpu_temp())
	labels, values = temperature_history()
	max_temp, min_temp, avg_temp = temperature_stats()
	return render_template("home.html", max_temp=max_temp, min_temp= min_temp, avg_temp=avg_temp, labels = labels, values = values)

@app.route('/temperature')
def temperature():
	cpu_temperature =  fetch_cpu_temp()
	store_temperature(cpu_temperature)  # Store temperature in DB
	return jsonify(temperature=cpu_temperature)




if __name__ == "__main__":
	app.run(host = "0.0.0.0", port = 8000)
