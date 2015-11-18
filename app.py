import urllib2, google
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
@app.route("/home")
@app.route("/home/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
   app.debug = True
   app.secret_key = "Secret secrets"
   app.run(host="0.0.0.0", port=9000)
