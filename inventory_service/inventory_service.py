# from fastapi import FastAPI, Query
# from dapr.actor import ActorInterface, Actor

# app = FastAPI()

# class Item(object):
#     def __init__(self, id, name, stock):
#         self.id = id
#         self.name = name
#         self.stock = stock

# # Replace with your Redis connection details
# state_store_name = "inventory"

# @Actor
# class InventoryActor(ActorInterface):
#     async def get_stock(self, item_id: str) -> int:
#         state = await app.dapr.get_state(state_store_name, item_id)
#         if state:
#             return int(state)
#         else:
#             return 0

#     async def reserve(self, item_id: str, quantity: int) -> bool:
#         state = await app.dapr.get_state(state_store_name, item_id)
#         if state and int(state) >= quantity:
#             new_stock = int(state) - quantity
#             await app.dapr.save_state(state_store_name, item_id, str(new_stock))
#             return True
#         else:
#             return False

# @app.get("/stock/{item_id}")
# async def check_stock(item_id: str = Query(..., description="ID of the item")):
#     stock = await InventoryActor.get_stock(item_id)
#     return {"item_id": item_id, "stock": stock}
from fastapi import FastAPI

from dapr.actor import ActorInterface, Actor

app = FastAPI()

class Item(object):
    def __init__(self, id, name, stock):
        self.id = id
        self.name = name
        self.stock = stock

# Replace with your Redis connection details
state_store_name = "inventory"


class InventoryActor(ActorInterface):
    async def get_stock(self, item_id: str) -> int:
        state = await app.dapr.get_state(state_store_name, item_id)
        if state:
            return int(state)
        else:
            return 0

    async def reserve(self, item_id: str, quantity: int) -> bool:
        state = await app.dapr.get_state(state_store_name, item_id)
        if state and int(state) >= quantity:
            new_stock = int(state) - quantity
            await app.dapr.save_state(state_store_name, item_id, str(new_stock))
            return True
        else:
            return False

@app.get("/stock/{item_id}")
async def check_stock(item_id: str):  # Remove Query argument
    stock = await InventoryActor.get_stock(item_id)
    return {"item_id": item_id, "stock": stock}