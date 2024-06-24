# from dapr.actor import Actor, ActorInterface, actormethod
# from dapr.actor.runtime.actor import ActorRuntime

# class InventoryActor(Actor, ActorInterface):
#     def __init__(self, ctx, actor_id):
#         super(InventoryActor, self).__init__(ctx, actor_id)

#     @actormethod(name="get_stock")
#     async def get_stock(self, item_id: str) -> int:
#         state = await self.state_manager.get_state(item_id)
#         if state:
#             return int(state)
#         else:
#             return 0

#     @actormethod(name="reserve")
#     async def reserve(self, item_id: str, quantity: int) -> bool:
#         state = await self.state_manager.get_state(item_id)
#         if state and int(state) >= quantity:
#             new_stock = int(state) - quantity
#             await self.state_manager.save_state(item_id, str(new_stock))
#             return True
#         else:
#             return False

# ActorRuntime.register_actor(InventoryActor)
from dapr.actor.runtime.context import ActorRuntimeContext
from dapr.actor import Actor
from dapr.actor import ActorRuntime
from dapr.actor import actormethod

class InventoryActor(Actor):
  def __init__(self, ctx: ActorRuntimeContext, actor_id: str):
    super().__init__(ctx, actor_id)

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

if __name__ == "__main__":
  import asyncio
# Get the running event loop (replace deprecated get_event_loop)
loop = asyncio.get_running_loop()
loop.run_until_complete(ActorRuntime.start())