import json
import redis

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# List of item IDs to verify
item_ids = ['item1', 'item2', 'item3']

# Verifying the stored data
print("Verifying stored data in Redis:")
for item_id in item_ids:
    # Retrieve the JSON string from Redis
    item_details_json = r.hget(item_id, 'details')
    if item_details_json:
        # Decode the JSON string back into a dictionary
        item_details = json.loads(item_details_json)
        # Print the decoded data
        print(f"{item_id}: {item_details}")
    else:
        print(f"{item_id}: No data found")
