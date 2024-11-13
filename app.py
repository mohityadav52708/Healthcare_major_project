from flask import Flask, jsonify, render_template
import random

app = Flask(__name__)

# Simulated dynamic cancer data for the top 10 states (replace this with actual data source)
states_data = [
    {"state": "Maharashtra", "cases": random.randint(80000, 120000)},
    {"state": "Tamil Nadu", "cases": random.randint(70000, 110000)},
    {"state": "Uttar Pradesh", "cases": random.randint(75000, 115000)},
    {"state": "Kerala", "cases": random.randint(60000, 100000)},
    {"state": "West Bengal", "cases": random.randint(65000, 105000)},
    {"state": "Karnataka", "cases": random.randint(68000, 108000)},
    {"state": "Gujarat", "cases": random.randint(70000, 110000)},
    {"state": "Rajasthan", "cases": random.randint(62000, 98000)},
    {"state": "Andhra Pradesh", "cases": random.randint(66000, 102000)},
    {"state": "Delhi", "cases": random.randint(68000, 106000)}
]

@app.route('/api/cancer-data')
def cancer_data_api():
    # Sort the states by the number of cases and get the top 10
    sorted_data = sorted(states_data, key=lambda x: x["cases"], reverse=True)
    top_10_states = sorted_data[:10]
    return jsonify(top_10_states)

@app.route('/')
def index():
    return render_template('home.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

if __name__ == "__main__":
    app.run(debug=True)
