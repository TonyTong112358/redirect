
from flask import Flask, g, render_template, request,redirect,make_response
import os
from flask_httpauth import HTTPBasicAuth
from paths.update import update_bp
import sqlite3

from utils import load_panel_value

DATABASE = "main.db"

app = Flask(__name__, template_folder='./templates')
auth = HTTPBasicAuth()
def init_db():
    conn = sqlite3.connect(DATABASE)
    with open('tables.sql', 'r') as f:
        conn.executescript(f.read())
    
    conn.commit()
    conn.close()

app.register_blueprint(update_bp)
@auth.verify_password
def verify_password(username, password):
  if username == os.getenv("ADMIN_USERNAME") and password == os.getenv("ADMIN_PASSWORD"):
      g.user = username
      return True
  return False



@app.route('/panel', methods=['GET', 'POST'])
@auth.login_required
def panel():
    response = load_panel_value()

    return render_template('panel.jinja', response=response,error= "")

    
@app.route('/redirect/<path:subpath>')
def home(subpath=None):
    try:
        with open("url.txt") as f:
            saved_url = f.read().strip()
    except FileNotFoundError:
        saved_url = None

    if saved_url:
        return redirect(saved_url, code=302)
    else:
        return redirect("http://example.com", code=302)
@app.route('/<path:subpath>')
def malicious_endpoint(subpath):
    values = load_panel_value()
    print(f"Received request for subpath: {subpath}")
    print(values["path"])
    
    if subpath != values["path"][1:]:
        return "resource Not Found", 404
    
    header_lines = values["header"].split("\n")
    
    response = make_response(values["body"],values["status_code"])
    for i in range(0, len(header_lines)):
        header_key = header_lines[i].split(":")[0].strip()
        header_value = header_lines[i].split(":")[1].strip()
        response.headers[header_key] = header_value

    return response

# @auth.login_required
# @app.route('/log', methods=['GET'])
# def log():
#     with sqlite3.connect("main.db") as conn:
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM logs")
#         logs = cursor.fetchall()
#     return render_template('log.jinja', logs=logs)


init_db()