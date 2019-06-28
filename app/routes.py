import json
import requests

from flask import render_template, request, jsonify
from app import app

@app.route('/')
@app.route('/main')
def index():

    return render_template('main.html')

@app.route('/process', methods=["POST"])
def test():

    question = request.form['question']

    #todo: question parser

    url = "https://en.wikipedia.org/w/api.php?format=json&action=query&" +\
        "prop=coordinates|extracts&exintro&explaintext&titles=" + question
    response = requests.get(url)
    found = json.loads(response.text)
    end_recur = 0

    while end_recur == 0:
        for key, value in found.items():
            if key == "coordinates":
                print(value)
                coordinates = value[0]
                lat = coordinates["lat"]
                longi = coordinates["lon"]
            elif key == "extract":
                summary = value
                end_recur = 1
            elif isinstance(value, dict):
                found = value

    return jsonify({'summary' : summary, 'lat' : lat, 'longi' : longi})
