import sys
import pickle
# import requests
from sklearn.tree import DecisionTreeRegressor

coffee = sys.argv[1]
pt = sys.argv[2]

def get_prediction():
    # url = 'https://cdn.glitch.com/97010f47-023e-493e-b71d-b283c5f1a1c7%2Fdtree.p?v=1607876471105'
    # r = requests.get(url, allow_redirects=True)

    # dtree = pickle.loads(r.content)
    dtree = pickle.load( open( "dtree.p", "rb" ))

    oup = dtree.predict([[coffee, pt]])
    return oup

print(get_prediction())