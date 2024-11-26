from flask import Flask, render_template, redirect, url_for, request
import requests as rq


app = Flask(__name__)

HOST = "localhost"
PORT = 50050
URL_BASE = f"http://{HOST}:{PORT}"

@app.route('/', methods=["GET"])
def index():
    # get all products
    res = rq.get(f"{URL_BASE}/api/products")
    # render them
    data = res.json()
    return render_template('index.html', data=data)

@app.route('/add', methods=["GET"])
def add():
    return render_template('add.html')

@app.route('/add', methods=["POST"])
def add_post():
    # construct form data into a shape we can send to server
    type_str = request.form['type'].capitalize()
    product_args = {}
    for key, value in request.form.items():
        if key != "type" and value != "":
            key_capped = key[0].capitalize() + key[1:]
            product_args[key_capped] = value

    # send form data to server
    res = rq.post(f"{URL_BASE}/api/product", 
                  json={"Type" : type_str, "Product" : product_args})

    print(res.status_code)
    
    return redirect(url_for('index'))