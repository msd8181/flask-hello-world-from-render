import sqlite3
from flask import Flask, g

DATABASE = 'db/database.db'
db_name  = DATABASE.rsplit('/')[-1]

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
