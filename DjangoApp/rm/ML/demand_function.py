import tensorflow as tf
import numpy as np
from tensorflow.keras.models import load_model

model = load_model('rm/ML/demand_prediction.h5')

def demand_pred(quantity, inventory, max_price, min_price, category):
    category_dict = {'Electrical Appliances': 0, 'Gadgets & Electronics': 1, 'Housewares': 2, 'Mother & Baby': 3, 'Personal Care & Health': 4, 'Pets': 5, 'Skincare & Makeup': 6, 'Sports & Travel': 7, 'Supermarket': 8, 'Toys & Books': 9}
    category = category.name
    ll = np.zeros((10,), dtype = int)
    prices = np.arange(int(min_price), int(max_price), 0.1)
    if category in list(category_dict.keys()):
        ll[category_dict[category]] = 1
    ll = np.array(ll).reshape(1, -1)
    demands = []
    for price in prices:
        prediction = model.predict(np.array([[price, *ll[0]]]))
        demands.append(prediction[0][0])

    price_demand_pairs = list(zip(prices, demands))
    sorted_price_demand_pairs = sorted(price_demand_pairs, key=lambda x: x[0], reverse=True)
    idx = 0
    demand_limit = quantity + inventory
    last = None

    for i, pair in enumerate(sorted_price_demand_pairs):
        if demand_limit <= 0:
            break
        if demand_limit <= pair[1]:
            last = (pair[0], demand_limit)
            idx = i
            break
        demand_limit = demand_limit - pair[1]
        idx = i

    if last is not None:
        sorted_price_demand_pairs[idx] = last

    # Get the optimal solution
    # Extract prices and demands into separate lists
    optimal_prices = [pair[0] for pair in sorted_price_demand_pairs]
    optimal_demands = [pair[1] for pair in sorted_price_demand_pairs]

    optimal_revenue = sum([price * demand for price, demand in sorted_price_demand_pairs])

    prices = prices.tolist()

    return prices, demands, optimal_prices, optimal_demands, optimal_revenue