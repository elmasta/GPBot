# -*- coding: Utf-8 -*

import json
from qparser import *

from flask import render_template, request, jsonify
from app import app

@app.route("/")
@app.route("/main")
def index():

    return render_template("main.html")

@app.route('/process', methods=["POST"])

def process():

    question = request.form["question"]
    p_response = RequestParser()

    p_response.string_to_list(question)
    with open("fr.json") as json_file:
        stop_word = json.load(json_file)
    p_response.request_reading(stop_word)
    if p_response.matchlist.count(1) != 0:
        p_response.stop_word_remover(stop_word)
        p_response.map_url_get(json)
        p_response.wiki_url_get(json)
        p_response.geocoding_researcher()
        p_response.wiki_researcher()
        p_response.quote_picker()
    return jsonify({"summary" : p_response.summary,
                    "quote" : p_response.quote,
                    "lat" : p_response.coordinates["lat"],
                    "longi" : p_response.coordinates["lng"],
                    "formatted_adress" : p_response.formatted_adress,
                    "error" : p_response.error})
