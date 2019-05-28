from flask import Flask, jsonify, render_template, request
import skyscanner_app
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
	render_template('search.html')

	out_date_start= request.args.get('out_date_start')
	out_date_end= request.args.get('out_date_end')
	in_date_start= request.args.get('in_date_start')
	in_date_end= request.args.get('in_date_end')
	out_city= request.args.get('out_city')
	in_city= request.args.get('in_city')
	data = [out_date_start,out_date_end,in_date_start,in_date_end,out_city,in_city]
	for i in range(len(data)):
		data[i] = str(data[i])
	for d in data:
		print type(d),d
	print "data ::: ",data
	res = skyscanner_app.get_data(data)
	min_data = skyscanner_app.get_cheapest(res)

	return render_template('skyscanner_result.html',data = min_data)

@app.route("/about")
def about():
	return "<h1>About page</h>"

if __name__ =='__main__':
	app.run(debug=True)