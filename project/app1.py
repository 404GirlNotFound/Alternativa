from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__, template_folder="templates1", static_folder="static1")
app.secret_key = os.urandom(24)

notes = []

@app.route('/add_note', methods=['POST'])
def add_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        notes.append({'title': title, 'content': content})
        return redirect(url_for('index'))


@app.route('/delete_note/<int:note_id>')
def delete_note(note_id):
    notes.pop(note_id)
    return redirect(url_for('index'))

@app.route('/')
def index():
    return render_template('index.html', notes=notes)

if __name__ == "__main__":
    app.run(debug=True, port=5000)