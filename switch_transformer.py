import torch
from labml.transformers.mha import MultiHeadAttention
from labml_nn.transformers.feed_forward import FeedForward
from labml_nn.utils import clone_module_list
from torch import nn


class SwitchFeedForward(nn.Module):
    def __init__(
        self,
        *,
        capacity_factor: float,
        drop_tokens: bool,
        is_scale_prob: bool,
        n_experts: int,
        expert: FeedForward,
        d_model: int,
    ):
        super().__init__()
        self.capacity_factor = capacity_factor
        self.is_scale_prob = is_scale_prob
        self.n_experts = n_experts
        self.drop_tokens = drop_tokens

        self.experts = clone_module_list(expert, n_experts)

        self.switch = nn.Linear(d_model, n_experts)
        self.softmax = nn.Softmax(dim=-1)

    def forward(self, x: torch.Tensor):
        seq_len, batch_size, d_model = x.shape
        x = x.view(-1, d_model)
        route_prob = self.softmax(self.switch(x))
        route_prob_max, routes = torch.max(route_prob, dim=-1)
        indexes_list = [
            torch.eq(routes, i).nonzero(as_tuple=True)[0] for i in range(self.n_experts)
        ]
        final_output = x.new_zeros(x.shape)
        capacity = int(self.capacity_factor * len(x) / self.n_experts)
        counts = x.new_tensor([len(indexes_list[i]) for i in range(self.n_experts)])
        dropped = []
