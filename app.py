from flask import Flask, jsonify, render_template, request

#Backend
import unirest
import json
#import unirest
app = Flask(__name__)


@app.route("/")
@app.route("/home")
def hello():
	return render_template('home.html')

@app.route("/skyscanner")
def skyscanner():
	return render_template('skyscanner_appHome.html')

@app.route("/search",methods = ['POST', 'GET'])
def skyscanner_search():
	out_date= request.args.get('out_date_start')
	render_template('search.html',out_date_start=out_date)

	return render_template('skyscanner_result.html')

@app.route("/about")
def about():
	return "<h1>About page</h>"

if __name__ =='__main__':
	app.run(debug=True)