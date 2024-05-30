# from dapr.actor import ActorInterface, Actor

# class InventoryActor(ActorInterface):
#     def __init__(self):
#         self.state_store_name = "inventory"

#     async def get_stock(self, item_id: str) -> int:
#         # Retrieve stock quantity for the given item_id from the state store
#         state = await self.actor_state.get_state(self.state_store_name, item_id)
#         if state:
#             return int(state)
#         else:
#             return 0

#     async def reserve(self, item_id: str, quantity: int) -> bool:
#         # Reserve specified quantity of items
#         current_stock = await self.get_stock(item_id)
#         if current_stock >= quantity:
#             new_stock = current_stock - quantity
#             await self.actor_state.save_state(self.state_store_name, item_id, str(new_stock))
#             return True
#         else:
#             return False
from dapr.actor import Actor, ActorInterface, actormethod
from dapr.actor.runtime.actor import ActorRuntime

class InventoryActor(Actor, ActorInterface):
    def __init__(self, ctx, actor_id):
        super(InventoryActor, self).__init__(ctx, actor_id)

    @actormethod(name="get_stock")
    async def get_stock(self, item_id: str) -> int:
        state = await self.state_manager.get_state(item_id)
        if state:
            return int(state)
        else:
            return 0

    @actormethod(name="reserve")
    async def reserve(self, item_id: str, quantity: int) -> bool:
        state = await self.state_manager.get_state(item_id)
        if state and int(state) >= quantity:
            new_stock = int(state) - quantity
            await self.state_manager.save_state(item_id, str(new_stock))
            return True
        else:
            return False

ActorRuntime.register_actor(InventoryActor)