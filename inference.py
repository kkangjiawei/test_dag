from ray import serve
from fastapi import FastAPI
from predictor import Predictor
from omegaconf import OmegaConf
from starlette.requests import Request
from typing import Dict
import os

app = FastAPI()

@serve.deployment(route_prefix="/inference")
class MyModel:
    def __init__(self) -> None:
        self.cfg = OmegaConf.load(os.path.join(os.path.dirname(__file__), "config.yaml"))
        #self.predictor = Predictor(selfcfg)
    
    async def __call__(self, request: Request) -> Dict:
        a = os.path.join(os.path.dirname(__file__), self.cfg.model_path)
        returun  a

model = MyModel.bind()
