from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__, template_folder="templates1", static_folder="static1")
app.secret_key = os.urandom(24)

users = []
notes = []

@app.route('/add_note', methods=['POST'])
def add_note():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        notes.append({'username' : session['username'] 'title': title, 'content': content})
        return redirect(url_for('index'))


@app.route('/delete_note/<int:note_id>')
def delete_note(note_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    user_notes_ids = []

    for i in range(len(notes)):
        if notes[i]['username'] == session['username']:
            user_notes_ids.append(i)
    
    if 0<= note_id < len(user_notes_ids):
        real_index = user_notes_ids[note_id]
        notes.pop(real_index)
    
    return redirect(url_for('index'))

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    user_notes = []
    
    for note in notes:
        if note['username'] == session["username"]:
            user_notes.append(note)
    
    return render_template('index.html', notes=user_notes, username=session['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        for user in users:
            if user['username'] == username and user['password'] == password:
                session['username'] = username
                return redirect(url_for('index'))
        
        return "Napačno uporabniško ime ali geslo."
            
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)