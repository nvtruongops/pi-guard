import sys
import json
from pathlib import Path
from datasets.arrow_dataset import Column
from transformers import PreTrainedTokenizerBase
import torch
from torch.utils.data import TensorDataset, default_collate

sys.path.insert(0, r"D:/Work/Do-an/workspaces/truongnv/replications/PromptShield_Jacob_CCS2024/PromptShield")
from utils.data_collections.benchmark_datasets import BenchmarkDataset

_original_tokenizer_call = PreTrainedTokenizerBase.__call__

def _accept_datasets_column(self, text, text_pair=None, *args, **kwargs):
    if isinstance(text, Column):
        text = list(text)
    if isinstance(text_pair, Column):
        text_pair = list(text_pair)
    if kwargs.get("truncation") and "max_length" not in kwargs:
        kwargs["max_length"] = 512
    return _original_tokenizer_call(self, text, text_pair, *args, **kwargs)

PreTrainedTokenizerBase.__call__ = _accept_datasets_column

_original_data_loader = torch.utils.data.DataLoader

def _trim_batch_padding(batch):
    collated = default_collate(batch)
    if isinstance(collated, (tuple, list)) and len(collated) == 3:
        input_ids, attention_mask, labels = collated
        if torch.is_tensor(attention_mask) and attention_mask.ndim == 2:
            max_tokens = int(attention_mask.sum(dim=1).max().item())
            return (input_ids[:, :max_tokens], attention_mask[:, :max_tokens], labels)
    return collated

class _DynamicPaddingDataLoader(_original_data_loader):
    def __init__(self, *args, **kwargs):
        if kwargs.get("collate_fn") is None:
            kwargs["collate_fn"] = _trim_batch_padding
        super().__init__(*args, **kwargs)

torch.utils.data.DataLoader = _DynamicPaddingDataLoader

_original_get_labels = BenchmarkDataset.get_labels
_eval_order = None

def _labels_in_eval_order(self):
    labels = _original_get_labels(self)
    if _eval_order is not None and len(labels) == len(_eval_order):
        return labels[_eval_order]
    return labels

BenchmarkDataset.get_labels = _labels_in_eval_order

_original_data_loader_init = _DynamicPaddingDataLoader.__init__

def _sorted_dynamic_init(self, dataset, *args, **kwargs):
    global _eval_order
    if isinstance(dataset, TensorDataset) and len(dataset.tensors) == 3 and dataset.tensors[1].ndim == 2:
        lengths = dataset.tensors[1].sum(dim=1)
        _eval_order = torch.argsort(lengths, stable=True)
        dataset = TensorDataset(*(tensor.index_select(0, _eval_order) for tensor in dataset.tensors))
        Path.cwd().joinpath("promptshield_eval_row_order.json").write_text(
            json.dumps(_eval_order.tolist()), encoding="utf-8"
        )
    _original_data_loader_init(self, dataset, *args, **kwargs)

_DynamicPaddingDataLoader.__init__ = _sorted_dynamic_init
print("compatibility adapter: Column -> list[str], max_length=512, length-bucketed batches, trim batch padding; row permutation recorded", file=sys.stderr)
