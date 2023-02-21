import ray
import requests
import sys
# sys.path.append(r"/mnt/work/features")
from fastapi import FastAPI
from ray import serve
from pydantic import BaseModel
import torch
import os
import esm
import numpy as np
# os.chdir("/mnt/work/featurespeppi")
sys.path.append("...")
from utils.process_feature import extract_tokens
# ray.init("auto", runtime_env={"working_dir": "/mnt/work/features"})
app = FastAPI()

a1 = 111
class Items(BaseModel):
    prot_or_pep: list
# @serve.deployment(route_prefix="/kk")

# class extract_tokens():
#
#     def __init__(self, esm_mode: bool, max_len = int):
#         """_summary_
#
#         Args:
#             esm_mode (Bool): esm_mode = True for extraction features in ESM
#         """
#         self.char2id = {'A': 5, 'C': 23, 'D': 13, 'E': 9, 'F': 18, 'G': 6, 'H': 21, 'I': 12, 'K': 15, 'L': 4, 'M': 20, 'N': 17, 'P': 14, 'Q': 16, 'R': 10, 'S': 8, 'T': 11, 'V': 7, 'W': 22, 'Y': 19, 'X':24, 'B':25, 'O':28, 'U':26, 'Z':27, 'BOS': 0, 'EOS':2}
#         self.id2char = {v:k for k,v in self.char2id.items()}
#         self.esm_mode = esm_mode
#         self.max_len = max_len
#
#     def __call__(self, sequences):
#
#         # token map in ESM, 25 letters without 'J', 'BeginOfSequence','EndOfSequence','Padding' are 0,2,1 respectively.
#         sequences = [_[:self.max_len] for _ in sequences]
#         if self.esm_mode:
#             batch_lens = [len(seq)+2 for seq in sequences]
#         else:
#             batch_lens = [len(seq) for seq in sequences]
#
#         tokens = np.ones((len(sequences), max(batch_lens)), dtype = np.int64)
#         for i, seq in enumerate(sequences):
#             if self.esm_mode:
#                 tmp = [self.char2id["BOS"]] + [self.char2id[c] for c in seq]  + [self.char2id["EOS"]] # without 'BeginOfSequence' and 'EndOfSequence'
#             else:
#                 tmp = [self.char2id[c] for c in seq]
#             tokens[i,:len(tmp)] = tmp
#         return tokens

def load_prot_esm(model_path, device):

    model_name = "esm2_t12_35M_UR50D"
    # load the model
    model_data = torch.load(os.path.join(model_path, "{}.pt".format(model_name)),map_location="cpu")
    regression_data = torch.load(os.path.join(model_path, '{}-contact-regression.pt'.format(model_name)))
    model, _ = esm.pretrained.load_model_and_alphabet_core(model_name, model_data, regression_data)
    model.to(device)
    model.eval()  # disables dropout for deterministic results
    return model

def get_device(device_ids):
    device = torch.device(
        "cuda:{}".format(device_ids[0]) if torch.cuda.is_available()
        and len(device_ids) > 0 else "cpu")
    return device
def get_aa_online_features(item_dict):
    # item_dict = item_dict.dict()
    # prot_or_pep = str(item_dict['prot_or_pep'])

    return f"1111Hello from " + item_dict + "!"

@serve.deployment(route_prefix="/hello")
@serve.ingress(app)
class MyFastAPIDeployment:
    @app.get("/")
    def root(self):
        return "Hello, world!"

    @app.post("/features")
    def root(self, item_dict: Items):
        tmp = item_dict.dict()
        sequences = tmp["prot_or_pep"]
        a = extract_tokens(esm_mode=True, max_len=529)
        batch_tokens = a(sequences)
        batch_tokens = torch.from_numpy(batch_tokens)
        DEVICE = get_device([1])
        os.chdir('/mnt/work/features')
        ab = os.getcwd()
        model = load_prot_esm("./pretrained_models/protein/esm2_t12", DEVICE)
        with torch.no_grad():
            batch_tokens = batch_tokens.to(DEVICE)
            try:
                results = model(batch_tokens, repr_layers=[12], return_contacts=False)
            except:
                print("-----------------")
            token_representations = results["representations"][12].cpu().numpy()
        return token_representations


myfastapi = MyFastAPIDeployment.bind()
# serve.run(MyFastAPIDeployment.bind())
# resp = requests.post("http://localhost:8000/hello/Serve")
# assert resp.json() == "Hello from Serve!"
