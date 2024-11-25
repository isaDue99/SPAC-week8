from flask import Flask, render_template
import requests as rq


app = Flask(__name__)

HOST = "localhost"
PORT = 50050
URL_BASE = f"http://{HOST}:{PORT}"

@app.route('/')
def main(data=None):
    # get all products
    res = rq.get(f"{URL_BASE}/api/products")
    # render them
    data = res.json()
    return render_template('main.html', data=data)