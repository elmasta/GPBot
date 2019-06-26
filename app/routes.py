from flask import render_template, request, jsonify
from app import app

@app.route('/')
@app.route('/main')
def index():

    return render_template('main.html')

@app.route('/process', methods=["POST"])
def test():

    question = request.form['question']
    question += "a"
    return jsonify({'question' : question})
