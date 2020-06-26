# pylint: disable=invalid-name

from flask import Flask, request, render_template, send_from_directory
from app.utils import Application
import threading

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('home.html')

@app.route('/statics/<path:path>')
def send_statics(path):
    return send_from_directory('statics', path)

@app.route("/refresh")
def refresh():
    app = Application()
    print("Thread refreshed started ...")
    threading.Thread(target=app.refresh, args=())
    return render_template('refresh.html')

@app.route("/team", methods=['POST'])
def team():
    app = Application()
    result = app.team(request.form.to_dict(flat=True))
    return render_template('team.html', result=result)

if __name__ == "__main__":
    app.run()