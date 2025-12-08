from datetime import datetime 
from flask import Flask, g, render_template, request,redirect,make_response
import os
from flask_httpauth import HTTPBasicAuth
from paths.update import update_bp
import sqlite3

from utils import *

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


@app.route('/')
def index():
    try:
        with open("url.txt") as f:
            saved_url = f.read().strip()
    except FileNotFoundError:
        saved_url = None

    if saved_url:
        return redirect(saved_url, code=302)
    else:
        return redirect("http://example.com", code=302)
@app.route('/panel', methods=['GET', 'POST'])
@auth.login_required
def panel():
    response = load_panel_value()

    return render_template('panel.jinja', response=response,error= "")

    
@app.route('/redirect/<path:subpath>')
def home(subpath=None):
    saved_url = get_redirect_url()

    if saved_url:
        return redirect(saved_url, code=302)
    else:
        return redirect("http://example.com", code=302)
@app.after_request
def after_request(response):
    request_method = request.method
    request_ip = request.remote_addr
    request_headers = dict(request.headers)
    request_body = request.data.decode('utf-8')
    request_arguments = request.args.to_dict()
    request_time = datetime.now()
    request_path = request.path
    store_logs(request_time, request_ip, request_method, str(request_headers), request_body, str(request_arguments), request_path)
    return response

@app.route('/<path:subpath>')
def malicious_endpoint(subpath):
    values = load_panel_value()
    print(f"Received request for subpath: {subpath}")
    print(values["path"])
    #  log everything 
    

    
    if subpath != values["path"][1:]:
        return "resource Not Found", 404
    
    header_lines = values["header"].split("\n")
    
    response = make_response(values["body"],values["status_code"])
    for i in range(0, len(header_lines)):
        header_key = header_lines[i].split(":")[0].strip()
        header_value = header_lines[i].split(":")[1].strip()
        response.headers[header_key] = header_value

    return response

@auth.login_required
@app.route(f'{LOGS_DIRECTORY}', methods=['GET'])
def log():
    
    count = request.args.get("limit", default=10, type=int)
    logs = get_logs(count)
    return render_template('logs.jinja', logs=logs)



@auth.login_required
@app.post("/add_note/<int:log_id>")
def add_note(log_id):
    notes = request.form.get("notes", "")

    db = get_db()
    db.execute(
        "UPDATE logs SET notes = ? WHERE ID = ?",
        (notes, log_id)
    )
    db.commit()

    return redirect(request.referrer or f'{LOGS_DIRECTORY}')


init_db()