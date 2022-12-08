import pandas as pd
import numpy as np

def prodList():
    products = pd.read_csv("dataset/products.csv")
    aisles = pd.read_csv("dataset/aisles.csv")
    departments = pd.read_csv("dataset/departments.csv")

    products = products.merge(aisles, on='aisle_id').merge(departments, on='department_id')
    products = products.sort_values('product_id')
    products = products[:1000]
    products = products.to_numpy().tolist()
    return products