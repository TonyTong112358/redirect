from flask import Blueprint, request, redirect, render_template
from utils import get_db, load_panel_value, LOGS_DIRECTORY, REDIRECT_DIRECTORY

update_bp = Blueprint('update', __name__, template_folder='./templates')


@update_bp.route('/update/redirect', methods=['POST'])
def update_redirect():
    url = request.form.get('url', '')
    db = get_db()
    cursor = db.cursor()
    cursor.execute("REPLACE INTO redirect_url (id, url) VALUES (1, ?)", (url,))
    db.commit()
    response = load_panel_value()

    return render_template('panel.jinja', response=response,error= "")

@update_bp.route('/update/response', methods=['POST'])
def update_response():
    path = request.form.get('path', '')
    header = request.form.get('header', '')
    body = request.form.get('body', '')
    status_code = request.form.get('status_code', '')

    response = load_panel_value()
    if(path == "/" or path == "" or path == LOGS_DIRECTORY or path.startswith(REDIRECT_DIRECTORY)):
        return render_template('panel.jinja', response=response,error = "footgun detected ")

    header_check = header.split("\n")
    
    if status_code == "" or not status_code.isnumeric():
        return render_template('panel.jinja', response=response,error = "status code must be a number")
    for h in header_check:
        if len(h.split(":")) !=2:
            return render_template('panel.jinja', response=response,error = "Invalid header format, each line must have one key:value")
    db = get_db()
    cursor = db.cursor()

    cursor.execute("REPLACE INTO Response (id, header,directory,body,status_code) VALUES (1, ?, ?, ?, ?)", (header, path, body, status_code))
    db.commit()
    response = load_panel_value()
    


    
    return render_template('panel.jinja', response=response,error = "")