from flask import Flask, render_template, request, jsonify, request
import main
import os

app = Flask(__name__)
party_dict, grid = main.initial_run()

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/party', methods=['POST'])
def select_party():	
	print(request)
	print('<iframe src="'+request.url_root+'map" name="targetframe" allowTransparency="true" scrolling="no" style="width:650px;height:600px" >')
	main.print_map(request.get_json()['party-name'], party_dict, grid)
	return '<iframe src=templates/index.html name="targetframe" allowTransparency="true" scrolling="no" style="width:650px;height:600px" >'

@app.route('/map')
def show_map():
	return render_template('map.html')


if __name__ == '__main__':
	app.debug = True
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)
