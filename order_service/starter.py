from dapr.clients import DaprClient

# Define constants
STATE_STORE_NAME = "statestore"

async def startup():
    # Connect to Dapr runtime on startup
    global dapr_client
    dapr_client = DaprClient()
