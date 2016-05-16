from flask import render_template, request
from app import app


@app.route('/')
def homepage():
    name = request.args.get('name')
    number = request.args.get('number')
    if not name:
        name = '<unknown>'
    return render_template('Homepage.html', name=name, number=number)

