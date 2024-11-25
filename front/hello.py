from flask import Flask, render_template
import requests as rq


app = Flask(__name__)

HOST = "localhost"
PORT = 50050
URL_BASE = f"http://{HOST}:{PORT}"

@app.route('/')
@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None, data=None):
    # insert product
    rq.post(f"{URL_BASE}/api/product", json={"Type": "Product", "Product": dict(
        Name="testProduct", 
        Description="Test description", 
        Quantity=1, 
        Price=1.00
    )})
    rq.post(f"{URL_BASE}/api/product", json={"Type": "Product", "Product": dict(
        Name="aaaa", 
        Description="Test description", 
        Quantity=100, 
        Price=69.00
    )})
    rq.post(f"{URL_BASE}/api/product", json={"Type": "Product", "Product": dict(
        Name="bluhhhh", 
        Description="Test description", 
        Quantity=1, 
        Price=1.00
    )})
    # get all products
    res = rq.get(f"{URL_BASE}/api/products")
    # render them
    data = res.json()
    return render_template('hello.html', person=name, data=data)