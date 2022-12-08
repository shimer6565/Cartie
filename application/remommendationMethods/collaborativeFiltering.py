import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from application.remommendationMethods.orders_products_df import ordersProducts
from application.remommendationMethods.products import prodList


def cf(query_index):
    products = prodList()
    products = pd.DataFrame(products, columns =['product_id', 'product_name', 'aisle_id', 'department_id', 'aisle', 'department'])
    orders_products_df = ordersProducts()
    orders_products_df_matrix = csr_matrix(orders_products_df.values)
    
    model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
    model_knn.fit(orders_products_df_matrix)

    distances, indices = model_knn.kneighbors(orders_products_df.iloc[query_index,:].values.reshape(1, -1), n_neighbors = 13)

    reco = []
    for i in range(len(distances.flatten())):
        reco.append(orders_products_df.index[indices.flatten()[i]])
    reco = pd.DataFrame(reco, columns=['product_name'])
    reco = reco.merge(products, on='product_name')
    swap_list = ["product_id","product_name","aisle_id","department_id", "aisle", "department"]
    reco = reco.reindex(columns=swap_list)
    return reco