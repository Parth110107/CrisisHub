from flask import Flask, render_template, request, redirect
import sqlite3
from flask import flash


app = Flask(__name__)
app.secret_key = 'crisishub_secret'


# ---------- DATABASE INITIALIZATION ----------
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Volunteers table
    c.execute('''CREATE TABLE IF NOT EXISTS Volunteers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    contact TEXT NOT NULL,
                    skills TEXT,
                    availability TEXT
                )''')

    # Requests table
    c.execute('''CREATE TABLE IF NOT EXISTS Requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    requester_name TEXT NOT NULL,
                    contact TEXT NOT NULL,
                    resource_type TEXT,
                    description TEXT,
                    location TEXT,
                    urgency TEXT
                )''')

    conn.commit()
    conn.close()


# ---------- HOME ----------
@app.route('/')
def index():
    return render_template('index.html')


# ---------- ADD VOLUNTEER ----------
@app.route('/add_volunteer', methods=['GET', 'POST'])
def add_volunteer():
    if request.method == 'POST':
        flash("Volunteer registered successfully!", "success")

        name = request.form['name']
        contact = request.form['contact']
        skills = request.form['skills']
        availability = request.form['availability']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO Volunteers (name, contact, skills, availability) VALUES (?, ?, ?, ?)",
                  (name, contact, skills, availability))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add_volunteer.html')


# ---------- ADD REQUEST ----------
@app.route('/add_request', methods=['GET', 'POST'])
def add_request():
    if request.method == 'POST':
        requester_name = request.form['requester_name']
        contact = request.form['contact']
        resource_type = request.form['resource_type']
        description = request.form['description']
        location = request.form['location']
        urgency = request.form['urgency']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''INSERT INTO Requests (requester_name, contact, resource_type, description, location, urgency)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (requester_name, contact, resource_type, description, location, urgency))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add_request.html')


# ---------- VIEW DATA ----------
@app.route('/view')
def view_data():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("SELECT * FROM Volunteers")
    volunteers = c.fetchall()

    c.execute("SELECT * FROM Requests")
    requests = c.fetchall()

    conn.close()
    return render_template('view_data.html', volunteers=volunteers, requests=requests)


# ---------- SEARCH VOLUNTEER BY SKILL ----------
@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        skill = request.form['skill']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM Volunteers WHERE skills LIKE ?", ('%' + skill + '%',))
        results = c.fetchall()
        conn.close()
    return render_template('search.html', results=results)

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM Volunteers")
    volunteers = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM Requests")
    requests = c.fetchone()[0]

    conn.close()
    return render_template(
        'dashboard.html',
        volunteers=volunteers,
        requests=requests
    )



# ---------- MAIN ----------
if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0", port=5000)


