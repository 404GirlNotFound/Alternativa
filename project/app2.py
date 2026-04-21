from flask import Flask, render_template, request, redirect, session, url_for
from tinydb import TinyDB, Query
import os
import uuid

app = Flask(__name__, template_folder="templates2", static_folder="static2")
app.secret_key = os.urandom(24)


db = TinyDB("db2/db.json")
users = db.table("users")
posts = db.table("posts")

User = Query()
Post = Query()

@app.route("/")
def index():
    if "username" not in session:
        return redirect(url_for("login"))
    
    all_posts = posts.all()
    all_posts.reverse()
    return render_template("index.html", posts=all_posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if users.search(User.username == username):
            return "Ta uporabnik že obstaja"
            
        users.insert({'username': username, 'password': password})
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users.get(User.username == username)

        if user and user['password'] == password:
            session['username'] = username
            return redirect(url_for('index'))
        
        return "Napačno uporabniško ime ali geslo."
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route("/add_post", methods=["POST"])
def add_post():
    if "username" not in session:
        return redirect(url_for("login"))

    content = request.form["content"]
    image = request.files.get("image")

    filename = ""

    if image:
        filename = str(uuid.uuid4()) + "_" + image.filename
        image.save("static2/uploads/" + filename)

    posts.insert({
        "username": session["username"],
        "content": content,
        "image": filename,
        "likes": 0
    })

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=5001)