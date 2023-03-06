def optimizer(prices, demands, quantity_produced, inventory, min_price, max_price):
    if len(prices) != len(demands):
        return "wrong"
    
    num = len(prices)

    for i in range(num - 1, -1, -1):
        # min_price & max_price
        if prices[i] > max_price:
            del prices[i]
            del demands[i]
            continue

        if prices[i] < min_price:
            del prices[i]
            del demands[i]
            continue
    
    #Demand constraint
    price_demand_pairs = list(zip(prices, demands))
    sorted_price_demand_pairs = sorted(price_demand_pairs, key=lambda x: x[0], reverse=True)
    idx = 0
    demand_limit = quantity_produced + inventory
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

    # Calculate revenue
    optimal_revenue = sum([price * demand for price, demand in sorted_price_demand_pairs])


    # Return the optimal solution
    return optimal_revenue, optimal_prices, optimal_demands