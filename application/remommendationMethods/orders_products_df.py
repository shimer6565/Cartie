import pandas as pd
from application.remommendationMethods.products import prodList

def ordersProducts():
    order_products_train = pd.read_csv("dataset/order_products__train.csv")
    products = prodList()
    products = pd.DataFrame(products, columns =['product_id', 'product_name', 'aisle_id', 'department_id', 'aisle', 'department'])
    orders_products = order_products_train.merge(products, on='product_id')
    orders_products.rename(columns = {'add_to_cart_order':'rating'}, inplace = True)

    print(orders_products.columns)
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

    orders_products_df=rating_popular_products.pivot_table(index='product_name',columns='order_id',values='rating').fillna(0)
    return orders_products_df