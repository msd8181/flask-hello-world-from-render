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

# this is just a temp thing for now
@app.route("/names")
def names():
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT Timestamp, language, problem FROM table1 ORDER BY Timestamp DESC")
        rows = cur.fetchall()
        conn.close()
    except Exception as e:
        rows = []
        error = f"❌ Error fetching data: {e}"
        return render_template_string("<p>{{ error }}</p>", error=error)

    html_list = """
    <!doctype html>
    <html>
      <head><title>All Entries</title></head>
      <body>
        <h2>Entries in Database</h2>
        {% if rows %}
          <table border="1" cellpadding="5" cellspacing="0">
            <tr><th>Timestamp</th><th>Language</th><th>Problem</th></tr>
            {% for row in rows %}
              <tr>
                <td>{{ row[0] }}</td>
                <td>{{ row[1] }}</td>
                <td>{{ row[2] }}</td>
              </tr>
            {% endfor %}
          </table>
        {% else %}
          <p>No entries found.</p>
        {% endif %}
        <p><a href="/form">Add another entry</a></p>
      </body>
    </html>
    """
    return render_template_string(html_list, rows=rows)


if __name__ == '__main__':
    app.run(debug=True)
