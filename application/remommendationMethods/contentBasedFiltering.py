import pandas as pd
import numpy as np
import pickle
from flask import url_for
from application.remommendationMethods.products import prodList
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel


def cbf(product_name):
  products = prodList()
  products = pd.DataFrame(products, columns =['product_id', 'product_name', 'aisle_id', 'department_id', 'aisle', 'department'])
  productsCopy = products.copy()


  tfv = TfidfVectorizer(min_df=3, max_features=None,
                      strip_accents='unicode', analyzer='word', token_pattern='\w{1,}',
                      ngram_range=(1,3),
                      stop_words='english')

  products['description'] = products.apply(lambda x : x[4] + ' ' + x[5], axis = 1)

  products['description'] = products['description'].fillna('')
  tfv_matrix = tfv.fit_transform(products['description'])
  sig = sigmoid_kernel(tfv_matrix, tfv_matrix)
  # sig = np.loadtxt('application/remommendationMethods/sigmoid.txt')
  # sig =  np.ndarray(sig)
  
  indices = pd.Series(products.index, index=products['product_name']).drop_duplicates()

  idx = indices[product_name]
  sig_scores = list(enumerate(sig[idx]))
  sig_scores = sorted(sig_scores, key = lambda x: x[1], reverse = True)
  sig_scores = sig_scores[1:13]
  product_indices = [i[0] for i in sig_scores]
  print(products['product_name'].iloc[product_indices])
  products = products['product_name'].iloc[product_indices]
  products = pd.DataFrame(products)
  products.index.names = ['product_id']
  print(products, productsCopy.columns)

  products = products.merge(productsCopy, on='product_id')
  return products