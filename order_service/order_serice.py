# Import necessary libraries
from dapr.clients import DaprClient

# Define constants
STATE_STORE_NAME = "statestore"
ORDER_STATE_PENDING = "pending"
ORDER_STATE_PROCESSED = "processed"
ORDER_STATE_SHIPPED = "shipped"

# Function to create a new order
async def create_order(order_details):
    try:
        # Connect to Dapr runtime
        with DaprClient() as d:
            # Save order details to state store with initial state as pending
            await d.save_state(STATE_STORE_NAME, order_details["order_id"], order_details, state=ORDER_STATE_PENDING)
            
            # Invoke Inventory Service to reserve items
            response = await d.invoke_service("inventory-service", "reserve-items", data=order_details)
            
            # Update order state to processed if item reservation is successful
            if response.status_code == 200:
                await d.save_state(STATE_STORE_NAME, order_details["order_id"], state=ORDER_STATE_PROCESSED)
            
            # Return success message
            return {"message": "Order created successfully"}
    
    except Exception as e:
        # Handle exceptions
        return {"error": str(e)}

# Function to cancel an order
async def cancel_order(order_id):
    try:
        # Connect to Dapr runtime
        with DaprClient() as d:
            # Check if order exists
            order_state = await d.get_state(STATE_STORE_NAME, order_id)
            if order_state:
                # Update order state to cancelled
                await d.save_state(STATE_STORE_NAME, order_id, state="cancelled")
                return {"message": "Order cancelled successfully"}
            else:
                return {"error": "Order not found"}
    
    except Exception as e:
        # Handle exceptions
        return {"error": str(e)}

# Main function to handle incoming requests
async def main(req):
    try:
        # Parse incoming request
        order_details = req.json()
        
        # Determine action based on request
        if req.method == "POST":
            # Create a new order
            return await create_order(order_details)
        elif req.method == "DELETE":
            # Cancel an existing order
            return await cancel_order(order_details["order_id"])
        else:
            return {"error": "Unsupported HTTP method"}
    
    except Exception as e:
        # Handle exceptions
        return {"error": str(e)}
