r"""Simple script to hook up a minimind configured model for inference.

Run with:

  uv run playground/inference.py

  or

  python3 playground/inference.py

Example output:

== results ==
x.shape = torch.Size([2, 8])
y.logits.shape = torch.Size([2, 8, 6400])
params:  1262272
== y: MoeCausalLMOutputWithPast ==
MoeCausalLMOutputWithPast(loss=None, aux_loss=tensor(0.), logits=tensor([[[-0.0274, -0.1229,  0.0540,  ..., -0.2226,  0.1078,  0.0136],
         [ 0.1471, -0.1027,  0.0504,  ..., -0.0305,  0.2095, -0.1706],
         [ 0.1434, -0.0520, -0.0378,  ..., -0.2586,  0.5319,  0.0833],
         ...,
         [ 0.2407,  0.0159, -0.4007,  ...,  0.1647, -0.1372, -0.0180],
         [ 0.0498,  0.1417, -0.1497,  ...,  0.0458,  0.2320, -0.0180],
         [ 0.1294, -0.1074, -0.1606,  ..., -0.0868, -0.1504,  0.2827]],

        [[-0.2884,  0.2626,  0.4419,  ...,  0.0130,  0.0548,  0.1903],
         [-0.1094,  0.0511,  0.2159,  ..., -0.0349,  0.2162,  0.2169],
         [-0.3383, -0.2448,  0.3213,  ..., -0.0968, -0.0979, -0.0612],
         ...,
         [-0.2916, -0.2512,  0.1799,  ..., -0.1456, -0.0475,  0.0210],
         [-0.0760, -0.3414,  0.2201,  ..., -0.2815, -0.0893,  0.0392],
         [-0.3578, -0.0632,  0.3890,  ..., -0.2189, -0.2816,  0.0052]]]), past_key_values=[None, None], hidden_states=tensor([[[ 0.7880, -1.7363, -0.3643,  ...,  0.5186, -0.2101, -0.2289],
         [ 0.6157, -1.4695,  0.4450,  ...,  0.2897, -0.2168,  0.1384],
         [-1.1906, -0.9376, -0.9560,  ...,  1.1631, -1.0426,  1.6791],
         ...,
         [-0.1053, -0.7113, -0.6749,  ...,  1.3753, -1.0547, -0.8988],
         [-0.3684, -0.7516, -0.6523,  ...,  2.2563, -1.9251,  0.4251],
         [ 0.0927, -1.6419, -0.9721,  ...,  1.6356, -0.6509, -1.3698]],

        [[-1.2491, -1.2869, -0.2852,  ..., -0.0069,  1.2842,  0.4436],
         [-1.2496, -1.2969, -0.8297,  ...,  0.0730,  1.5555,  0.3381],
         [-1.6230, -0.7450, -1.0231,  ..., -0.4243,  2.0940,  0.3060],
         ...,
         [-2.6554,  0.2832,  0.7186,  ..., -1.2833,  0.5278,  0.8033],
         [-1.9803, -0.5781,  0.8274,  ..., -0.1089,  0.9712, -0.0612],
         [-1.1460, -0.0896,  0.8875,  ..., -0.1872,  0.4759,  0.6574]]]), attentions=None, router_logits=None)
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import torch

from model.model_minimind import MiniMindConfig, MiniMindForCausalLM
from transformers.modeling_outputs import MoeCausalLMOutputWithPast

BATCH_SIZE = 2
SEQ_LEN = 8

if __name__ == "__main__":
    config = MiniMindConfig(
        hidden_size=128,
        num_hidden_layers=2,
    )
    model = MiniMindForCausalLM(config).eval()

    x: torch.FloatTensor = torch.randint(0, config.vocab_size, (BATCH_SIZE, SEQ_LEN))
    with torch.no_grad():
        y: MoeCausalLMOutputWithPast = model(x)

    print("== results ==")
    print(f"x.shape = {x.shape}")
    print(f"y.logits.shape = {y.logits.shape}")
    print("params: ", sum(p.numel() for p in model.parameters()))
    print("== y: MoeCausalLMOutputWithPast ==")
    print(y)
