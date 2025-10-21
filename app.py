from flask import Flask, request, render_template_string, g
import sqlite3
from datetime import datetime
import os

DATABASE = 'db/database.db'
db_name  = DATABASE.rsplit('/')[-1]

app = Flask(__name__)

DB_PATH = os.path.join("db", "database.db")

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    cur = get_db().cursor()
    if cur:
        return f'connected to {db_name} successfully!'
    return 'not connected!'

@app.route("/form", methods=["GET", "POST"])
def form():
    message = ""
    if request.method == "POST":
        language = request.form.get("language")
        problem = request.form.get("problem")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO table1 (Timestamp, language, problem) VALUES (?, ?, ?)",
                (timestamp, language, problem),
            )
            conn.commit()
            conn.close()
            message = "✅ Data added successfully!"
        except Exception as e:
            message = f"❌ Error: {e}"

    html_form = """
    <!doctype html>
    <html>
      <head>
        <title>Simple Form</title>
      </head>
      <body>
        <h2>Submit a New Entry</h2>
        <form method="POST">
          <label>Language:</label><br>
          <input type="text" name="language" required><br><br>

          <label>Problem:</label><br>
          <textarea name="problem" rows="4" cols="40" required></textarea><br><br>

          <input type="submit" value="Submit">
        </form>
        <p>{{ message }}</p>
      </body>
    </html>
    """

    return render_template_string(html_form, message=message)


if __name__ == '__main__':
    app.run(debug=True)
