# JailbreakBench source and local artifact status

The local harmful/benign behavior records were compared field-by-field with the two public CSVs at pinned Hugging Face revision `d8d87b8fdcb7806e3b4e45fffb2bc24aa6b17f32`. Each source/local CSV and JSON contains 100 records and every row field matches. Local serialized bytes differ from upstream; see [dataset provenance](../datasets/DATASET_PROVENANCE.md) and run [the row verifier](../verify_jbb_source_rows.py).

The former combined wrapper and the two copies of `JAILBREAKBENCH_REPLICATION_BENCHMARK_RESULTS.json` were removed. The old runner used ProtectAI’s prompt-injection classifier on behavior-goal text, then described positive flags as jailbreak detection. That setup did not evaluate attack success or JailbreakBench defense effectiveness. The runner now exits with a withdrawal notice.

The remaining upstream code snapshot is a reference package. Its presence does not certify paper reproduction.
