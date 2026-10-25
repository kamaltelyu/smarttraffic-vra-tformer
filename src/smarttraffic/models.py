import math
import torch
import torch.nn as nn
import torch.nn.functional as F

from .config import TRAFFIC_COLS, REL_COLS, PaperConfig

CFG = PaperConfig()
NT, NR, NO, DM = len(TRAFFIC_COLS), len(REL_COLS), CFG.n_horizons, CFG.d_model

class PositionalEncoding(nn.Module):
    def __init__(self, d_model=DM, max_len=2048):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        pos = torch.arange(max_len).unsqueeze(1).float()
        div = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(pos * div)
        pe[:, 1::2] = torch.cos(pos * div)
        self.register_buffer("pe", pe.unsqueeze(0), persistent=False)

    def forward(self, x):
        return x + self.pe[:, : x.size(1)]

class TransformerModel(nn.Module):
    def __init__(self, input_dim=NT):
        super().__init__()
        self.p = nn.Linear(input_dim, DM)
        self.pos = PositionalEncoding(DM)
        layer = nn.TransformerEncoderLayer(
            DM, CFG.n_head, DM * 4, CFG.dropout, batch_first=True, norm_first=True
        )
        self.e = nn.TransformerEncoder(layer, CFG.n_layers)
        self.h = nn.Sequential(nn.LayerNorm(DM), nn.Linear(DM, NO))

    def encode(self, x):
        return self.e(self.pos(self.p(x)))

    def forward(self, x, q=None):
        z = self.encode(x)
        return self.h(z.mean(dim=1))

class ReliabilityConcat(nn.Module):
    def __init__(self):
        super().__init__()
        self.m = TransformerModel(NT + NR)

    def forward(self, x, q):
        return self.m(torch.cat([x, q], dim=-1))

class ReliabilityAttentionLayer(nn.Module):
    def __init__(self):
        super().__init__()
        self.nh = CFG.n_head
        self.att = nn.MultiheadAttention(DM, self.nh, dropout=CFG.dropout, batch_first=True)
        self.n1 = nn.LayerNorm(DM)
        self.n2 = nn.LayerNorm(DM)
        self.ff = nn.Sequential(nn.Linear(DM, DM * 4), nn.GELU(), nn.Dropout(CFG.dropout), nn.Linear(DM * 4, DM))

    def forward(self, x, reliability=None, lam=None):
        mask = None
        if reliability is not None and lam is not None:
            b, length, _ = reliability.shape
            key_bias = lam * torch.log(reliability.squeeze(-1).clamp_min(1e-5))
            mask = key_bias[:, None, :].expand(b, length, length).repeat_interleave(self.nh, dim=0)
        h = self.n1(x)
        a, _ = self.att(h, h, h, attn_mask=mask, need_weights=False)
        x = x + a
        return x + self.ff(self.n2(x))

class VRATFormer(nn.Module):
    def __init__(self):
        super().__init__()
        self.obs = nn.Sequential(nn.Linear(NT, DM), nn.GELU())
        self.rel = nn.Sequential(nn.Linear(NR, DM // 2), nn.GELU())
        self.gate = nn.Sequential(nn.Linear(DM // 2, 1), nn.Sigmoid())
        self.ctx = nn.GRU(NT, DM, batch_first=True)
        self.pos = PositionalEncoding(DM)
        self.layers = nn.ModuleList([ReliabilityAttentionLayer() for _ in range(CFG.n_layers)])
        self.rawlam = nn.Parameter(torch.tensor(0.0))
        self.head = nn.Sequential(nn.LayerNorm(DM), nn.Linear(DM, NO))

    def forward(self, x, q):
        obs = self.obs(x)
        ctx, _ = self.ctx(x)
        r = self.gate(self.rel(q))
        z = r * obs + (1 - r) * ctx
        z = self.pos(z)
        lam = F.softplus(self.rawlam)
        for layer in self.layers:
            z = layer(z, r, lam)
        return self.head(z.mean(dim=1))

class RRTFormer(nn.Module):
    """Traffic-only inference with privileged reliability supervision during training."""
    def __init__(self, transformer_state=None):
        super().__init__()
        self.backbone = TransformerModel()
        if transformer_state is not None:
            self.backbone.load_state_dict(transformer_state)
        self.reconstruction_head = nn.Sequential(nn.Linear(DM, DM), nn.GELU(), nn.Linear(DM, NT))
        self.reliability_head = nn.Sequential(nn.Linear(DM, 32), nn.GELU(), nn.Linear(32, 1), nn.Sigmoid())

    def forward(self, x, return_aux=False):
        z = self.backbone.encode(x)
        pred = self.backbone.h(z.mean(dim=1))
        if not return_aux:
            return pred
        return {
            "pred": pred,
            "reconstructed": self.reconstruction_head(z),
            "reliability": self.reliability_head(z),
        }

def interpolate_state(state_a, state_b, alpha: float):
    """Linear checkpoint interpolation used by RB-TFormer."""
    out = {}
    for key, a in state_a.items():
        b = state_b[key]
        out[key] = ((1 - alpha) * a + alpha * b) if torch.is_floating_point(a) else a.clone()
    return out
