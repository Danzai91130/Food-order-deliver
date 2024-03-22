from collections import Counter
from collections import defaultdict
import datetime

def get_all_orders(db):
    """Retrieve all orders from the database."""
    orders_ref = db.collection('commandes_sandwichs').where('preparee', '==', True)
    orders = orders_ref.get()

    # Extract data from QuerySnapshot and convert to list of dictionaries
    orders_data = [order.to_dict() for order in orders]

    return orders_data


def analyze_orders(orders):
    """Analyze orders to find the most used ingredients, sauces, etc."""
    ingredients_count = {}
    sauces_count = {}
    proteines_count = {}

    for order in orders:
        for ingredient in order.get('ingredients', '').split(','):
            ingredients_count[ingredient.strip()] = ingredients_count.get(ingredient.strip(), 0) + 1
        for sauce in order.get('sauces', '').split(','):
            sauces_count[sauce.strip()] = sauces_count.get(sauce.strip(), 0) + 1
        for proteine in order.get('proteine', '').split(','):
            proteines_count[proteine.strip()] = proteines_count.get(proteine.strip(), 0) + 1

    most_used_ingredients = sorted(ingredients_count.items(), key=lambda x: x[1], reverse=True)[:5]
    most_used_sauces = sorted(sauces_count.items(), key=lambda x: x[1], reverse=True)[:5]
    most_used_proteines = sorted(proteines_count.items(), key=lambda x: x[1], reverse=True)[:5]

    return most_used_ingredients, most_used_sauces, most_used_proteines, ingredients_count, proteines_count, sauces_count

def calculate_average_order_size(orders):
    """Calculate the average number of ingredients, sauces, and proteines per order."""
    total_orders = len(orders)
    total_ingredients = sum(len(order.get('ingredients', '').split(',')) for order in orders)
    total_sauces = sum(len(order.get('sauces', '').split(',')) for order in orders)
    total_proteines = sum(len(order.get('proteine', '').split(',')) for order in orders)

    avg_ingredients_per_order = total_ingredients / total_orders
    avg_sauces_per_order = total_sauces / total_orders
    avg_proteines_per_order = total_proteines / total_orders

    return avg_ingredients_per_order, avg_sauces_per_order, avg_proteines_per_order

def identify_most_common_combinations(orders):
    """Identify the most common combinations of ingredients, sauces, and proteines."""
    # Initialize counters for ingredients, sauces, and proteines
    ingredients_counter = Counter()
    sauces_counter = Counter()
    proteines_counter = Counter()

    # Iterate over each order and update the counters
    for order in orders:
        ingredients_counter.update(order.get('ingredients', '').split(','))
        sauces_counter.update(order.get('sauces', '').split(','))
        proteines_counter.update(order.get('proteine', '').split(','))

    # Identify the most common combinations
    most_common_ingredients = ingredients_counter.most_common(3)
    most_common_sauces = sauces_counter.most_common(3)
    most_common_proteines = proteines_counter.most_common(3)

    return most_common_ingredients, most_common_sauces, most_common_proteines

def analyze_order_trends_over_time(orders):
    """Analyze trends in orders over time by hour."""
    # Initialize a defaultdict to store the count of orders per hour
    orders_per_hour = defaultdict(int)

    # Iterate over each order and update the count of orders for each hour
    for order in orders:
        # Extract the placement time from the order
        placement_time = order.get('placement_time')
        if placement_time:
            # Extract the hour from the placement time
            order_hour = datetime.datetime.strptime(placement_time, '%Y-%m-%d %H:%M:%S').hour
            # Increment the count of orders for the corresponding hour
            orders_per_hour[order_hour] += 1

    return orders_per_hour


def analyze_customer_insights(orders):
    """Analyze customer behavior."""
    # Initialize a defaultdict to store the count of orders per customer
    orders_per_customer = defaultdict(int)

    # Iterate over each order and update the count of orders for each customer
    for order in orders:
        # Extract the customer ID from the order
        customer_id = order.get('id_client')
        # Increment the count of orders for the corresponding customer
        orders_per_customer[customer_id] += 1

    # Sort customers by the number of orders they've made
    sorted_customers = sorted(orders_per_customer.items(), key=lambda x: x[1], reverse=True)

    return sorted_customers

def calculate_average_preparation_time(orders):
    """Calculate the average time taken to prepare orders."""
    total_preparation_time = 0
    total_orders = len(orders)

    # Iterate over each order and calculate the preparation time
    for i in range(1, total_orders):
        # Extract the order completion times for consecutive orders
        completion_time_prev = datetime.datetime.strptime(orders[i - 1].get('completion_time'), '%Y-%m-%d %H:%M:%S')
        completion_time_curr = datetime.datetime.strptime(orders[i].get('completion_time'), '%Y-%m-%d %H:%M:%S')

        # Calculate the preparation time between consecutive orders
        preparation_time = (completion_time_curr - completion_time_prev).seconds

        # Add the preparation time to the total
        total_preparation_time += preparation_time

    # Calculate the average preparation time
    avg_preparation_time = total_preparation_time / (total_orders - 1)  # Exclude the first order

    return avg_preparation_time
