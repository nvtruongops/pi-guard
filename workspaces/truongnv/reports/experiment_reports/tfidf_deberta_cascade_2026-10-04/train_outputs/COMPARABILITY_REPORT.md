# Comparability report

- The TF-IDF+LR comparator is the completed seed-42 model trained from the pinned PIDS-Bench author baseline code.
- The DeBERTa-v3 comparator is being fine-tuned from the pinned open `microsoft/deberta-v3-base` checkpoint with the pinned PIDS-Bench author training source and checksum-verified PIDS-Bench splits.
- The local run is a single seed and uses dynamic padding plus a resumed checkpoint. It is not the authors' five-seed aggregate and does not reproduce an undocumented historical checkpoint byte-for-byte.
- The cascade will be compared with these standalone runs on the same PIDS-Bench axes. Published DistilBERT means, if shown, will be kept separately labeled as paper-reported context rather than local same-seed measurements.

