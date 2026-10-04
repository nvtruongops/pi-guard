import torch
# from safetensors.torch import load_file
from PIGuard.modeling_piguard import PIGuard, PIGuardConfig
config = PIGuardConfig.from_pretrained("microsoft/deberta-v3-base")
config.num_labels = 2

model = PIGuard(config)

state_dict = torch.load("/home/hao/epoch_1_600_model.pth")
# state_dict = load_file("model.safetensors")
#model.load_state_dict(state_dict, strict=False)
model.save_pretrained("saves")