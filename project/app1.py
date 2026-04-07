from flask import Flask, render_template, request, redirect, session, url_for
from tinydb import TinyDB, Query
import os

app = Flask(__name__, template_folder="templates1", static_folder="static1")
app.secret_key = os.urandom(24)

db = TinyDB("db/db1.json")
users = db.table("users")
notes = db.table("notes")

User = Query()
Note = Query()

@app.route('/add_note', methods=['POST'])
def add_note():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        notes.insert({
            'username': session['username'],
            'title': title,
            'content': content
        })

        return redirect(url_for('index'))


@app.route('/delete_note/<int:note_id>')
def delete_note(note_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    user_notes = notes.search(Note.username == session['username'])
    
    if 0<= note_id < len(user_notes):
        note_delete = user_notes[note_id]
        notes.remove(doc_ids=[note_delete.doc_id])
    
    return redirect(url_for('index'))

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    user_notes = notes.search(Note.username == session['username'])
    
    return render_template('index.html', notes=user_notes, username=session['username'])

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

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/edit_note/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    user_notes = notes.search(Note.username == session['username'])

    if 0 <= note_id < len(user_notes):
        note_edit = user_notes[note_id]

        if request.method == 'POST':
            new_title = request.form['title']
            new_content = request.form['content']

            notes.update(
                {
                    'title': new_title,
                    'content': new_content
                },
                doc_ids=[note_edit.doc_id]
            )

            return redirect(url_for('index'))

        return render_template('edit_note.html', note=note_edit, note_id=note_id)

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, port=5000)