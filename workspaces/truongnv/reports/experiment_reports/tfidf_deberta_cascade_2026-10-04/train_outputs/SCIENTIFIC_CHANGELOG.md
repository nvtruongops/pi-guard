# Scientific and execution change log

- Continued the interrupted seed-42 PIDS-Bench DeBERTa-v3 fine-tune from durable checkpoint 3,388 using the same author source commit, public base checkpoint, frozen training split, FP32 precision, three-epoch schedule, and effective batch size 16.
- Used dynamic padding as a disclosed runtime adaptation; input text and labels were unchanged.
- Training reached the target global step 5,082. Test/OOD rows were not used for gradient updates or threshold selection.
- The first wrapper process saved the final model and Trainer checkpoint, then raised `UnicodeEncodeError` because the Windows CP1252 console could not encode `→` in a completion message. Artifact existence and checkpoint step were verified before recovery.
- Relaunched the author wrapper from checkpoint 5,082 with `PYTHONIOENCODING=utf-8` and `PYTHONUTF8=1`, using a fresh stage directory. The Trainer restored the final checkpoint and ran evaluation without repeating optimizer steps; the wrapper then recorded `status=completed`.
- The local TF-IDF → DeBERTa router was subsequently searched on validation only. Its frozen policy and held-out evaluation are recorded in `outputs/seed42/`; no paper is said to have proposed this router.
- The first matrix supports a call-reduction rationale on some measured axes but does not show improved hard-benign or structural-OOD robustness.
