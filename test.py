from flask import Flask, jsonify, render_template, request

#Backend
import requests
import json
#import unirest

api_key = '1c3b759866msh08fc8fcca0665b0p1efcfdjsn3fe94d77020c'
refurl = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/pricing/v1.0"
sessionkey = '1aed91cc-f931-4cae-b25d-c7ab95c905df'


headers={
    "X-RapidAPI-Host": "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
    "X-RapidAPI-Key": api_key,
    "Content-Type": "application/x-www-form-urlencoded"
  }
params={
    "Country": "US",
    "Currency": "USD",
    "Locale": "en-US",
    "OriginPlace": "SFO-sky",
    "DestinationPlace": "LHR-sky",
    "outboundpartialdate": "2019-09-01",
  }
# params=params
r_post = requests.post(refurl,headers=headers)


ref_url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0"
#ref_url="https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/US/USD/en-US/SFO-sky/JFK-sky/2019-10-01?inboundpartialdate=2019-09-01"

query= "/US/USD/en-US/SFO-sky/JFK-sky/2019-10-01"
params = {"inboundpartialdate":"2019-09-01"}
r = requests.get(ref_url+query,headers=headers,params=params)
print(r.url)

y = r.json()
print(type(y))

app = Flask(__name__)

posts = [
	{
		'author':'person1',
		'title': 'blog post 1'
	}
]

@app.route("/")
@app.route("/home")
def hello():
	return str(y["Places"])
	#error_handling(r,api_key)
	#render_template('home.html', posts=posts)

@app.route("/about")
def about():
	return "<h1>About page</h>"

if __name__ =='__main__':
	app.run(debug=True)