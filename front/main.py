from flask import Flask, render_template, redirect, url_for, request
import requests as rq


app = Flask(__name__)

HOST = "localhost"
PORT = 50050
URL_BASE = f"http://{HOST}:{PORT}"


@app.route('/', methods=["GET", "POST"])
def index():
    # if method was GET with id of product details to b displayed
    details = None
    if request.args:
        id = request.args["id"]
        res = rq.get(f"{URL_BASE}/api/product/{id}")
        details = eval(res.content)[0]

    # if method was post with either delete or update
    if request.method == "POST":
        id = request.form['id']
        if request.form['action'] == "delete":
            res = rq.delete(f"{URL_BASE}/api/product/{id}")

    # get all products
    res = rq.get(f"{URL_BASE}/api/products")
    data = res.json()

    return render_template('index.html', data=data, details=details)


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


@app.route('/update', methods=["GET"])
def update():
    id = request.args["id"]
    res = rq.get(f"{URL_BASE}/api/product/{id}")
    details = eval(res.content)[0]
    return render_template('update.html', details=details)

@app.route('/update', methods=["POST"])
def update_post():
    id = request.form['id']

    # construct form data into a shape we can send to server
    type_str = request.form['type'].capitalize()
    product_args = {}
    for key, value in request.form.items():
        if key not in "type, id" and value != "":
            key_capped = key[0].capitalize() + key[1:]
            product_args[key_capped] = value

    # send data to server
    rq.put(f"{URL_BASE}/api/product/{id}", 
           json={"Type" : type_str, "Product" : product_args})
    
    return redirect(url_for('index'))