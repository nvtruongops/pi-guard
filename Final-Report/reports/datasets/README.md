# Dataset initialization handoff

Ngày bàn giao: 2026-10-09. Đây là bản sao cục bộ cho Final-Report của split nghiên cứu v5 và bộ tài liệu/audit liên quan. Corpus và split nguồn trong workspace truongnv được giữ lại; một số dòng version log và audit được cập nhật để ghi rõ trạng thái split v5.

## Tuyên bố ranh giới nhiệm vụ

| IN-SCOPE | OUT-OF-SCOPE |
|---|---|
| Sao chép các split đã khóa và tài liệu provenance/audit để tiếp tục review dataset initialization. | Phê duyệt license hoặc taxonomy, huấn luyện, inference, báo cáo metric, commit/publish payload prompt. |

## Split đã bàn giao

Split group-aware nội bộ v5, trạng thái frozen_local_research_split, seed 42; tỷ lệ mục tiêu 70/15/15. Các tệp JSONL và ID được sao chép vào Final-Report/notebooks/data/splits/.

| Partition | Rows | JSONL SHA-256 |
|---|---:|---|
| Train | 28.280 | cb731d3e4392ca71a9fcd931949fd2f6ea38cb5a0ae0364d6aa261402ed260b2 |
| Validation | 5.858 | f449b92c74fd17e35ede07ce61dd8706e0965e733865226fff49364a963dfd10 |
| Test | 5.862 | 6114f589e73217393c5936f1613b4d1259953ba4518764c026428ec938435a37 |

Corpus source SHA-256: 2b6588e9aa091d536a25a878102df866090a2539f1bf5dbbd05d6ca6a7d09bfe. Full source corpus, workbook, source payload snapshots and builder scripts were not copied.

The split payload directory is ignored by Git at the repository root. These 7 files exist only in this local checkout and are not committed or published. Do not force-add the prompts.

## Research documents and metadata

- [Dataset inventory](research/urldata.md)
- [Corpus and split README](research/project_training/README.md)
- [Dataset version log](research/project_training/DATASET_VERSION_LOG.md)
- [Split manifest](research/project_training/splits/split_manifest.json)
- [Cross-source overlap audit](research/project_training/audit/cross_dataset_overlap.md)
- [Jailbreak source research](research/project_training/audit/jb_dataset_research.md)
- [Source dataset index](research/source_datasets/README.md)

The research mirror includes 28 Markdown documents and 10 non-prompt manifest/audit JSON files. Raw dataset files and upstream README copies were excluded. The documentation is present in the working tree and is not committed yet.

## Current research gate

The split records internal dataset initialization. Source-rights review and final three-label policy remain pending; PromptScreen still has row-level provenance/license caveats. No PI-Guard model was trained or evaluated from these files, and no independent benign/FPR holdout exists outside v5.

Validation before handoff: verify_balanced_corpus.py PASS; verify_dataset_bundle.py PASS; split_balanced_corpus.py --verify PASS. The copied split files were checked against their recorded hashes and row counts.
