import json
import requests
from qparser import *

from flask import render_template, request, jsonify
from app import app

@app.route('/')
@app.route('/main')
def index():

    return render_template('main.html')

@app.route('/process', methods=["POST"])

def process():

    lat = 0
    longi = 0
    error = 1
    summary = ""
    question = request.form['question']
    p_response = RequestParser()

    p_response.string_to_list(question)

    p_response_try = "".join(p_response.qprocess).replace("'", "")
    p_response_try = p_response_try.replace(")", "")
    p_response_try = p_response_try.replace("(", "")
    p_response_try = p_response_try.replace("-", "")

    if p_response_try.isalpha() is True:
        with open("fr.json") as json_file:
            stop_word = json.load(json_file)
        p_response.request_reading(stop_word)
        if p_response.matchlist.count(1) != 0:
            p_response.stop_word_remover(stop_word)
            url = "https://fr.wikipedia.org/w/api.php?format=json&action=query&" +\
                "prop=coordinates|extracts&exintro&explaintext&titles=" + p_response.qreturn
            response = requests.get(url)
            found = json.loads(response.text)
            end_recur = 0
            while end_recur == 0:
                for key, value in found.items():
                    if key == "coordinates":
                        coordinates = value[0]
                        lat = coordinates["lat"]
                        longi = coordinates["lon"]
                        error = 0
                    elif key == "extract":
                        summary = value
                        end_recur = 1
                    elif key == "missing":
                        end_recur = 1
                    elif isinstance(value, dict):
                        found = value

    return jsonify({'summary' : summary, 'lat' : lat, 'longi' : longi, "error" : error})
