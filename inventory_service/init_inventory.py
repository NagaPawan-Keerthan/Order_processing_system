import json
import redis

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Sample inventory data
inventory = {
    'item1': {'name': 'Laptop', 'quantity': 10, 'price': 1000, 'reserved': 0},
    'item2': {'name': 'Smartphone', 'quantity': 50, 'price': 500, 'reserved': 0},
    'item3': {'name': 'Tablet', 'quantity': 30, 'price': 300, 'reserved': 0},
}

# Storing inventory data in Redis
for item_id, item_details in inventory.items():
    # Convert the dictionary to a JSON string
    item_details_json = json.dumps(item_details)
    # Use hset to store the JSON string in Redis
    r.hset(item_id, 'details', item_details_json)

print("Inventory data has been initialized in Redis.")
