import os
from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# ✅ Database connection using DATABASE_URL
url = urlparse(os.getenv("DATABASE_URL"))

conn = mysql.connector.connect(
    host=url.hostname,
    user=url.username,
    password=url.password,
    database=url.path[1:],   # remove '/'
    port=url.port
)

cursor = conn.cursor(buffered=True)

@app.route('/')
def home():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    return render_template('index.html', students=students)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    age = int(request.form['age'])
    course = request.form['course']

    cursor.execute(
        "INSERT INTO students (name, age, course) VALUES (%s, %s, %s)",
        (name, age, course)
    )
    conn.commit()

    return redirect('/')
@app.route('/edit/<int:id>')
def edit(id):
    cursor.execute("SELECT * FROM students WHERE id=%s", (id,))
    student = cursor.fetchone()
    return render_template('edit.html', student=student)

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    name = request.form['name']
    age = request.form['age']
    course = request.form['course']

    cursor.execute(
        "UPDATE students SET name=%s, age=%s, course=%s WHERE id=%s",
        (name, age, course, id)
    )
    conn.commit()

    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    cursor.execute("DELETE FROM students WHERE id=%s", (id,))
    conn.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)