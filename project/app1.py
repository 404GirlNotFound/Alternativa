from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__, template_folder="templates1", static_folder="static1")
app.secret_key = os.urandom(24)

notes = []

@app.route('/')
def home():
    return ("neki")



if __name__ == "__main__":
    app.run(debug=True, port=5000)