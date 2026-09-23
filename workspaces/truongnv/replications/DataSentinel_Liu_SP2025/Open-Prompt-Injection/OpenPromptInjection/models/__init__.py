try:
    from .PaLM2 import PaLM2
except ImportError:
    PaLM2 = None

try:
    from .Vicuna import Vicuna
except ImportError:
    Vicuna = None

try:
    from .GPT import GPT, GPTAzure
except ImportError:
    GPT, GPTAzure = None, None

try:
    from .Llama import Llama
    from .Flan import Flan
    from .Internlm import Internlm
    from .QLoraModel import QLoraModel
    from .Llama3 import Llama3
    from .DeepSeek import DeepSeekWrapper, DeepSeekR1DistillLLaMAWrapper, DeepSeekR1DistillQwenWrapper
except ImportError:
    Llama, Flan, Internlm, QLoraModel, Llama3 = None, None, None, None, None
    DeepSeekWrapper, DeepSeekR1DistillLLaMAWrapper, DeepSeekR1DistillQwenWrapper = None, None, None


MODEL_REGISTRY = {
    'palm2': PaLM2,
    'vicuna': Vicuna,
    'gpt': GPT,
    'gpt_azure': GPTAzure,
    'llama': Llama,
    'llama3': Llama3,
    'mistral': QLoraModel,
    'flan': Flan,
    'internlm': Internlm,
}

QLORA_MODEL_REGISTRY = {
    'mistral': QLoraModel,
    'llama': QLoraModel,
    'llama3': Llama3,
}


def _create_deepseek(model_name, config):
    if 'distill' not in model_name:
        return DeepSeekWrapper(config)
    if 'llama' in model_name:
        return DeepSeekR1DistillLLaMAWrapper(config)
    if 'qwen' in model_name:
        return DeepSeekR1DistillQwenWrapper(config)
    raise ValueError(f"Unknown DeepSeek distillation base in model name {model_name!r}")


def create_model(config):
    """
    Factory method to create a LLM instance
    """
    provider = config["model_info"]["provider"].lower()
    model_name = config["model_info"]["name"].lower()
    if provider == 'deepseek':
        return _create_deepseek(model_name, config)
    try:
        model_class = MODEL_REGISTRY[provider]
    except KeyError as exc:
        raise ValueError(f"ERROR: Unknown provider {provider}") from exc
    return model_class(config)

def create_qlora_model(config):
    """
    Factory method to create a QLoRA LLM. See https://arxiv.org/abs/2305.14314 for details.
    """
    provider = config["model_info"]["provider"].lower()
    try:
        model_class = QLORA_MODEL_REGISTRY[provider]
    except KeyError as exc:
        raise ValueError(f"ERROR: Unknown provider {provider}") from exc
    return model_class(config)
