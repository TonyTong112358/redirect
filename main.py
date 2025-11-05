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

@app.before_request
def before_request():
    with open("url.txt") as f:
        g.url = f.read().strip()

@app.route('/panel', methods=['GET', 'POST'])
@auth.login_required
def panel():
    success_message = "Current URL: " + g.url
    if request.method == 'POST':
        url = request.form.get('url', '')
        with open("url.txt", "w") as f:
            f.write(url)
        
    return render_template('panel.jinja', success_message=success_message)

@app.route('/')
@app.route('/<path:subpath>')
def home(subpath=None):
    if(g.url):
        return redirect(g.url, code=302)
    else:
        return redirect("http://example.com", code=302)
    
