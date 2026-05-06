from flask import Flask, render_template, request, redirect, session, url_for
from tinydb import TinyDB, Query
import os

app = Flask(__name__, template_folder="templates3", static_folder="static3")

app.secret_key = os.urandom(24)

db = TinyDB("db3/db.json")

users = db.table("users")
books = db.table("books")

User = Query()
Book = Query()


@app.route("/")
def index():
    if "username" not in session:
        return redirect(url_for("login"))

    my_books = books.search(Book.username == session["username"])
    my_books.reverse()

    return render_template("index.html", books=my_books)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if users.get(User.username == username):
            return "Ta uporabnik že obstaja."

        users.insert({
            "username": username,
            "password": password
        })

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = users.get(User.username == username)

        if user and user["password"] == password:
            session["username"] = username
            return redirect(url_for("index"))

        return "Napačno uporabniško ime ali geslo."

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True, port=5003)