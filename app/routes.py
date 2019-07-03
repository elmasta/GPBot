import json
import requests
from qparser import f_parser

from flask import render_template, request, jsonify
from app import app

@app.route('/')
@app.route('/main')
def index():

    return render_template('main.html')

@app.route('/process', methods=["POST"])
def test():

    question = request.form['question']

    p_response = f_parser(question)

    if p_response == "error":
        lat = 0
        longi = 0
        summary = ""
        error = 1
    else:
        error = 0
        url = "https://fr.wikipedia.org/w/api.php?format=json&action=query&" +\
            "prop=coordinates|extracts&exintro&explaintext&titles=" + p_response
        response = requests.get(url)
        found = json.loads(response.text)
        end_recur = 0

        while end_recur == 0:
            for key, value in found.items():
                if key == "coordinates":
                    coordinates = value[0]
                    lat = coordinates["lat"]
                    longi = coordinates["lon"]
                elif key == "extract":
                    summary = value
                    end_recur = 1
                elif isinstance(value, dict):
                    found = value

    return jsonify({'summary' : summary, 'lat' : lat, 'longi' : longi, "error" : error})
