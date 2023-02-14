from ray import serve
import logging
from starlette.requests import Request
from ray.serve.handle import RayServeDeploymentHandle
from ray.serve.drivers import DAGDriver
from ray.serve.deployment_graph import InputNode

logger = logging.getLogger("ray.serve")


@serve.deployment
class FruitMarket:
    def __init__(
        self,
        say_hello: RayServeDeploymentHandle,
        say_bye: RayServeDeploymentHandle,
    ):
        self.directory = {
            "HELLO": say_hello,
            "BYE": say_bye,
        }
    async def check_price(self, fruit: str, amount: float) -> float:
        if fruit not in self.directory:
            return -1
        else:
            fruit_stand = self.directory[fruit]
            return await (await fruit_stand.remote(amount))
        
        
@serve.deployment
class SayHello:
    async def __call__(self, request: Request) -> str:
        logger.info("Hello world!")
        return "hi"
    
@serve.deployment
class SayBye:
    async def __call__(self, request: Request) -> str:
        logger.info("Hello world!")
        return "bye bye"

with InputNode() as query:
    fruit, amount = query[0], query[1]
    say_hello = SayHello.bind()
    say_bye = SayBye.bind()
    fruit_market = FruitMarket.bind(say_hello, say_bye)
    net_price = fruit_market.check_price.bind(fruit, amount)
deployment_graph = DAGDriver.bind(net_price, http_adapter=json_resolver)
