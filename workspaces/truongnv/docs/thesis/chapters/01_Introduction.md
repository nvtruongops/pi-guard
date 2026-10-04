# Chapter 1: Introduction

## 1.1 Background of the Study

Large language models (LLMs) are used through applications that place instructions and user requests into a model context. Some applications also add text from documents, web pages, or other external sources. This makes natural-language input part of the application’s security boundary. [[2]](#ref2) [[3]](#ref3) [[4]](#ref4)

Prompt injection is an attempt to make an LLM application follow an unintended instruction. Perez and Ribeiro (2022) studied direct attacks in which a user supplies text that redirects the model’s task or asks it to reveal part of the prompt. They describe **Goal Hijacking** [[TN1]](#term-goal-hijacking) and **Prompt Leaking** [[TN2]](#term-prompt-leaking) as two attack goals. [[3]](#ref3)

Greshake et al. (2023) examined indirect prompt injection, where an attacker places instructions in external content that an application later retrieves or processes. Their work shows how the attack path can reach a model without the attacker submitting the malicious text through the application’s direct user interface. [[4]](#ref4)

Jailbreak prompts seek to bypass safety restrictions that a model is intended to follow. Wei et al. (2023) describe **Competing Objectives** [[TN3]](#term-competing-objectives) and **Mismatched Generalization** [[TN4]](#term-mismatched-generalization) as two hypotheses for why safety training can fail on some adversarial requests. These are explanations studied by those authors, not proof that every model or jailbreak behaves in the same way. [[5]](#ref5)

These studies identify risks in particular models, prompts, and application settings. They motivate evaluating an additional screening layer while leaving the target model’s own safety behavior and the application’s access controls as separate concerns. The Prompt Guard model card also recommends combining model-based filtering with other protections. [[3]](#ref3) [[4]](#ref4) [[20]](#ref20)

## 1.2 Problem Statement

The PI-Guard project is registered as an external machine-learning guardrail for LLM applications. The project record describes classifying incoming prompts as benign, prompt injection, or jailbreak, then allowing, blocking, or flagging them before they reach the target LLM. ([Project Register](../../../../../CAPSTONE%20PROJECT%20REGISTER.md))

Those labels need an explicit annotation policy. “Direct” and “indirect” describe how attack text reaches an application, while “jailbreak” describes an attempt to bypass a model’s safety restrictions; one example can therefore fit more than one description. [[3]](#ref3) [[4]](#ref4) [[20]](#ref20) The project’s data objective also refers more generally to benign and malicious prompts, so the mapping from source labels to project labels must be documented before model results are interpreted. ([Project Register](../../../../../CAPSTONE%20PROJECT%20REGISTER.md))

The research problem is to develop and evaluate a text classifier that can support this guardrail under a clearly defined label policy and a reproducible evaluation protocol. Published studies use different attack settings and evaluation units, so their reported results cannot by themselves establish PI-Guard’s performance. [[23]](#ref23) [[34]](#ref34) [[30]](#ref30)

## 1.3 Research Objectives

The objectives below follow the project registration. They describe intended work; this chapter does not claim that the objectives have been completed. ([Project Register](../../../../../CAPSTONE%20PROJECT%20REGISTER.md))

**General objective**

Develop and implement a machine-learning guardrail to detect and mitigate prompt injection and jailbreak attacks in LLM applications.

**Specific objectives**

1. Curate and label benign and malicious prompts from public sources.
2. Design, train, and evaluate classical machine-learning and fine-tuned transformer classifiers for prompt classification.
3. Integrate a trained classifier as an API-driven guardrail that can block or flag malicious prompts before they reach the target LLM.
4. Evaluate detection accuracy, false-positive rates, and robustness to obfuscated and novel attack techniques.

## 1.4 Significance of the Study

The study’s academic value is its planned examination of how dataset labels, classifier choices, and evaluation procedures affect a prompt-screening task. Its contribution must be supported by the project’s own data and experiments rather than inferred from results reported for other systems. ([Project Register](../../../../../CAPSTONE%20PROJECT%20REGISTER.md)) [[23]](#ref23) [[30]](#ref30)

The intended practical value is an API layer that can inspect text before it is forwarded to an LLM. This layer can inform an application’s allow, block, or review decision. Authorization, data access, and tool permissions remain responsibilities of the application ([Threat Model](../../architecture/THREAT_MODEL_AND_ATTACK_SURFACE.md)). ([Project Register](../../../../../CAPSTONE%20PROJECT%20REGISTER.md)) [[20]](#ref20)

## 1.5 Scope and Limitations

| Boundary | Scope of this study |
|---|---|
| Security problem | Text-based prompt injection and jailbreak attempts in LLM applications, with benign inputs included for evaluating false alarms. ([Project Register](../../../../../CAPSTONE%20PROJECT%20REGISTER.md)) [[3]](#ref3) [[4]](#ref4) [[20]](#ref20) |
| Label policy | The registered project names benign, prompt-injection, and jailbreak outputs. Direct and indirect delivery paths require annotation rules that explain overlaps and ambiguous examples. ([Project Register](../../../../../CAPSTONE%20PROJECT%20REGISTER.md)) [[3]](#ref3) [[4]](#ref4) |
| System boundary | An external classifier inspects text presented to the guardrail before a request reaches the target LLM. The study does not assume access to the target model’s weights or internal state. ([Project Register](../../../../../CAPSTONE%20PROJECT%20REGISTER.md)) |
| Evaluation | The registered plan evaluates classifiers and the guardrail using labeled public data, including detection accuracy, false-positive rates, and robustness. Results apply only to the documented data, labels, and protocol used in each experiment. ([Project Register](../../../../../CAPSTONE%20PROJECT%20REGISTER.md)) |
| Limitations | A text classifier cannot by itself establish real-world attack prevalence, inspect content that never reaches its input, or enforce the application’s authorization and tool-use policies. These limits follow from the external text-inspection boundary. [[4]](#ref4) [[20]](#ref20) |

The scope table states the project’s research boundary. It does not report a completed three-class classifier, a completed cascade, or achieved performance targets. Such claims require results from the corresponding implementation and evaluation.

## 1.6 Thesis Structure

The thesis follows the chapter structure in the official FPT IAP491 guide. Chapter 1 introduces the problem, objectives, significance, scope, and organization. Chapter 2 reviews previous studies, summarizes the literature, and positions the project’s contribution. Later chapters describe the methodology, implementation and results, discussion, and conclusion. ([Official FPT IAP491 Guide](../../../../../docs/fpt_capstone_guide/IAP491_CP_StudentsGuideForm%20for%20Research%20Based%20Thesis.docx))

## BẢNG THUẬT NGỮ & KHÁI NIỆM HỌC THUẬT NỀN TẢNG (ACADEMIC CONCEPT GLOSSARY)

| Mã neo | Thuật ngữ và bản dịch | Định nghĩa khoa học | Vai trò trong PI-Guard | Nguồn |
|---|---|---|---|---|
| <a id="term-goal-hijacking"></a>TN1 | Goal Hijacking (chiếm hướng mục tiêu) | An attack that redirects a model from the application’s intended task toward an attacker-selected output. | A direct prompt-injection goal considered when defining attack labels. | Perez and Ribeiro (2022). [[3]](#ref3) |
| <a id="term-prompt-leaking"></a>TN2 | Prompt Leaking (làm lộ prompt) | An attempt to make a model reveal some or all of the prompt that was supplied to guide its task. | A disclosure-oriented attack example; the classifier’s label policy must distinguish it from ordinary requests to summarize visible text. | Perez and Ribeiro (2022). [[3]](#ref3) |
| <a id="term-competing-objectives"></a>TN3 | Competing Objectives (mục tiêu cạnh tranh) | A hypothesized safety-training failure in which model capabilities and safety goals conflict on a request. | A literature explanation for some jailbreak behaviors; not a claim about every PI-Guard input. | Wei et al. (2023). [[5]](#ref5) |
| <a id="term-mismatched-generalization"></a>TN4 | Mismatched Generalization (khái quát hóa không khớp) | A hypothesized failure in which safety training does not generalize to a domain where the model retains relevant capabilities. | Helps frame why evaluation should include varied attack forms, without claiming that PI-Guard has tested them all. | Wei et al. (2023). [[5]](#ref5) |

## References

The numeric anchors follow the local [References Log](../../../References/REFERENCES_LOG.md). Local PDFs are linked for source review.

<a id="ref2"></a>**[2]** Long Ouyang et al. “Training Language Models to Follow Instructions with Human Feedback.” NeurIPS 2022. [Local PDF](../../../References/Ouyang_2022_InstructGPT_Training_Language_Models_Follow_Instructions.pdf).

<a id="ref3"></a>**[3]** Fábio Perez and Ian Ribeiro. “Ignore Previous Prompt: Attack Techniques For Language Models.” NeurIPS Workshop on Machine Learning Safety, 2022. [Local PDF](../../../References/Perez_2022_Ignore_This_Title_Hack_This_Paper_Prompt_Injection.pdf).

<a id="ref4"></a>**[4]** Kai Greshake et al. “Not What You’ve Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection.” ACM AISec, 2023. [Local PDF](../../../References/Greshake_2023_Indirect_Prompt_Injection.pdf).

<a id="ref5"></a>**[5]** Alexander Wei, Nika Haghtalab, and Jacob Steinhardt. “Jailbroken: How Does LLM Safety Training Fail?” NeurIPS 2023. [Local PDF](../../../References/Wei_2024_Jailbroken_How_LLM_Safety_Training_Fails.pdf).

<a id="ref20"></a>**[20]** Meta AI. “Prompt Guard 86M Model Card.” 2024. [Local model card PDF](../../../References/Meta_2024_Prompt_Guard_86M_Input_Guardrail.pdf).

<a id="ref23"></a>**[23]** Jingwei Yi et al. “Benchmarking and Defending Against Indirect Prompt Injection Attacks on Large Language Models.” KDD 2025, pp. 1809–1820. arXiv:2312.14197. [arXiv record](https://arxiv.org/abs/2312.14197) · [Local PDF](../../../References/Viet_2024_BIPIA_Benchmarking_Indirect_Prompt_Injection_Attacks.pdf).

<a id="ref34"></a>**[34]** Patrick Chao et al. “JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models.” NeurIPS Datasets and Benchmarks Track, 2024. [Local PDF](../../../References/Chao_2024_JailbreakBench_Open_Robustness_Benchmark_NeurIPS.pdf).

<a id="ref30"></a>**[30]** Dennis Jacob et al. “PromptShield: Deployable Detection for Prompt Injection Attacks.” CODASPY, 2025. [arXiv record](https://arxiv.org/abs/2501.15145) · [Local PDF](../../../References/Jacob_2025_PromptShield_Deployable_Detection_CODASPY.pdf).
