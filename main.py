from flask import Flask, g, render_template, request,redirect
import os
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__, template_folder='.')
auth = HTTPBasicAuth()
@auth.verify_password
def verify_password(username, password):
  if username == os.getenv("ADMIN_USERNAME") and password == os.getenv("ADMIN_PASSWORD"):
      g.user = username
      return True
  return False



@app.route('/panel', methods=['GET', 'POST'])
@auth.login_required
def panel():
    if request.method == 'POST':
        url = request.form.get('url', '')
        with open("url.txt", "w") as f:
            f.write(url)
    try:
        with open("url.txt") as f:
            saved_url = f.read().strip()
        success_message = "Current URL: " + saved_url
    except FileNotFoundError:
        success_message = "No URL set."

    return render_template('panel.jinja', success_message=success_message)

@app.route('/')
@app.route('/<path:subpath>')
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
