from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__, template_folder="templates2", static_folder="static2")
app.secret_key = os.urandom(24)

posts = []

@app.route('/')
def index():
    return render_template('index.html', posts=posts)


if __name__ == "__main__":
    app.run(debug=True, port=5001)