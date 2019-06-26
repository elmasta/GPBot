from flask import render_template
from app import app

@app.route('/')
@app.route('/main')

def index():
    return render_template('main.html')