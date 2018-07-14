import flask
from flask import Flask, render_template, request, jsonify, request
import main

app = Flask(__name__)
party_dict, grid = main.initial_run()

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/party', methods=['POST'])
def select_party():	
	main.print_map(request.form['party-name'], party_dict, grid)
	return render_template('map.html')


if __name__ == "__main__":
	app.run(port = 5000, debug = True)