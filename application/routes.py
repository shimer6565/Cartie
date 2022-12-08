import pandas as pd
from application import app
from flask import Flask, render_template, request, redirect, url_for
from application.remommendationMethods.collaborativeFiltering import cf
from application.remommendationMethods.contentBasedFiltering import cbf
from application.remommendationMethods.pearsonsRCorrelation import prc
from application.remommendationMethods.products import prodList
from application.remommendationMethods.orders_products_df import ordersProducts


@app.route('/',methods=['POST','GET'])

def home():
    return render_template('home.html', items = prodList())

@app.route('/collaborativeFiltering',methods=['POST','GET'])

def collaborativeFiltering():
    products = prodList()
    products = pd.DataFrame(products, columns =['product_id', 'product_name', 'aisle_id', 'department_id', 'aisle', 'department'])
    orders_products_df = ordersProducts()
    finalProducts = pd.DataFrame(orders_products_df.index).merge(products, on='product_name')
    swap_list = ["product_id","product_name","aisle_id","department_id", "aisle", "department"]
    finalProducts = finalProducts.reindex(columns=swap_list)
    finalProductsList = finalProducts.to_numpy().tolist()
    if request.method == 'POST' and request.form.get('button') != "refresh":
        product = finalProducts.index[finalProducts['product_id'] == int(request.form.get('button'))]
        result = cf(product)
        item = result["product_name"][0]
        result = result[1:]
        return render_template('home.html', recommendation = result.to_numpy().tolist(), route = "/collaborativeFiltering", items = finalProductsList, cart = item)
    return render_template('home.html', recommendation = [], route = "/collaborativeFiltering", items = finalProductsList)

@app.route('/contentBasedFiltering',methods=['POST','GET'])

def contentBasedFiltering():
    if request.method == 'POST' and request.form.get('button') != "refresh":
        products = prodList()
        products = pd.DataFrame(products, columns =['product_id', 'product_name', 'aisle_id', 'department_id', 'aisle', 'department'])
        product = products["product_name"][int(request.form.get('button'))-1]
        result = cbf(product)
        return render_template('home.html', recommendation = result.to_numpy().tolist(),route = "/contentBasedFiltering", items = prodList(), cart = product)
    return render_template('home.html', recommendation = [], route = "/contentBasedFiltering", items = prodList())

@app.route('/pearsonsRCorrelation',methods=['POST','GET'])

def pearsonsRCorrelation():
    if request.method == 'POST':
        result = prc()
        return render_template('home.html', recommendation = result, items = prodList())
    return render_template('home.html', recommendation = [], route = "/pearsonsRCorrelation", items = prodList())

