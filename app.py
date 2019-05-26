from flask import Flask, render_template
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
	return render_template('home.html', posts=posts)

@app.route("/about")
def about():
	return "<h1>About page</h>"

if __name__ =='__main__':
	app.run(debug=True)