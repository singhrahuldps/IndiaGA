from flask import Flask, render_template, request, jsonify, request
import main
import os

app = Flask(__name__)
party_dict, grid = main.initial_run()

html = '<html></html>'

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/party', methods=['POST'])
def select_party():	
	html = main.print_map(request.get_json()['party-name'], party_dict, grid)
	return html

if __name__ == '__main__':
	app.debug = True
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)
