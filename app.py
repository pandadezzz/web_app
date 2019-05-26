from flask import Flask, render_template

response = unirest.post("https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/pricing/v1.0",
  headers={
    "X-RapidAPI-Host": "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
    "X-RapidAPI-Key": "1c3b759866msh08fc8fcca0665b0p1efcfdjsn3fe94d77020c",
    "Content-Type": "application/x-www-form-urlencoded"
  },
  params={
    "inboundDate": "2019-09-10",
    "cabinClass": "business",
    "children": 0,
    "infants": 0,
    "country": "US",
    "currency": "USD",
    "locale": "en-US",
    "originPlace": "SFO-sky",
    "destinationPlace": "LHR-sky",
    "outboundDate": "2019-09-01",
    "adults": 1
  }
)


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
	return response
	#render_template('home.html', posts=posts)

@app.route("/about")
def about():
	return "<h1>About page</h>"

if __name__ =='__main__':
	app.run(debug=True)