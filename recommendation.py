import pandas as pd
import numpy as np

orders = pd.read_csv("orders.csv")
departments = pd.read_csv("departments.csv")
aisles = pd.read_csv("aisles.csv")
order_products_prior = pd.read_csv("order_products__prior.csv")
products = pd.read_csv("products.csv")
sample = pd.read_csv("sample_submission.csv")
order_products_train = pd.read_csv("order_products__train.csv")

products = products.merge(aisles, on='aisle_id').merge(departments, on='department_id')
products = products.sort_values('product_id')

#collaborative filtering

orders_products = order_products_train.merge(products, on='product_id')
orders_products = orders_products[:1000000]
orders_products.rename(columns = {'add_to_cart_order':'rating'}, inplace = True)

orders_products = orders_products.dropna(axis = 0, subset = ['product_name'])
ratingCount = (orders_products.
     groupby(by = ['product_name'])['rating'].
     count().
     reset_index().
     rename(columns = {'rating': 'totalRatingCount'})
     [['product_name', 'totalRatingCount']]
    )

orders_products_with_totalRatingCount = orders_products.merge(ratingCount, left_on = 'product_name', right_on = 'product_name', how = 'left')
rating_threshold_min = 0
rating_threshold_max = 50
rating_popular_products= orders_products_with_totalRatingCount.query('totalRatingCount >= @rating_threshold_min')
rating_popular_products= orders_products_with_totalRatingCount.query('totalRatingCount <= @rating_threshold_max')
print(pd.unique(rating_popular_products['product_id']).size, rating_popular_products['order_id'].shape)

## First lets create a Pivot matrix

orders_products_df=rating_popular_products.pivot_table(index='product_name',columns='order_id',values='rating').fillna(0)
print(orders_products_df.shape)

from scipy.sparse import csr_matrix

orders_products_df_matrix = csr_matrix(orders_products_df.values)

from sklearn.neighbors import NearestNeighbors


model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
model_knn.fit(orders_products_df_matrix)