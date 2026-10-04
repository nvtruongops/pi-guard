# Chapter 2: Literature Review

## 2.1 Review Scope and Key Terms

This chapter reviews research on prompt injection and jailbreak attacks, benchmark design, and model-based detection. It follows the official FPT IAP491 guide’s direction to organize previous studies by theme and describe how the field has developed. ([Official FPT IAP491 Guide](../../../../../docs/fpt_capstone_guide/IAP491_CP_StudentsGuideForm%20for%20Research%20Based%20Thesis.docx))

Perez and Ribeiro (2022) study direct prompt injection, where attack text is supplied through the user’s interaction with an application. They call the goal of redirecting the task **Goal Hijacking** [[TN1]](#term-goal-hijacking) and the goal of extracting the original prompt **Prompt Leaking** [[TN2]](#term-prompt-leaking). [[3]](#ref3) Greshake et al. (2023) study indirect prompt injection, where attack text is placed in external content that an application later processes. [[4]](#ref4) Meta’s Prompt Guard model card describes jailbreaks as malicious instructions intended to override a model’s built-in safety features. [[20]](#ref20)

This review uses “direct” and “indirect” to describe the path by which text reaches an application, and “jailbreak” to describe an attack goal against the model’s safety behavior. These dimensions can overlap; the project therefore needs a written annotation rule before treating its registered labels as mutually exclusive classes. This is a project taxonomy decision informed by the attack definitions in the cited work. [[3]](#ref3) [[4]](#ref4) [[20]](#ref20) ([Project Register](../../../../../CAPSTONE%20PROJECT%20REGISTER.md))

## 2.2 Review of Previous Studies

### 2.2.1 Attack mechanisms and threat characterization

Perez and Ribeiro introduced a framework for studying prompt attacks and examined two goals: redirecting the model’s task and eliciting the original prompt. Their paper establishes concrete direct-attack examples, while its experiments do not estimate how often such attacks occur in deployed applications. [[3]](#ref3)

Greshake et al. extended the threat model to content that an LLM application retrieves or processes. Their demonstrations show that text supplied through an external source can influence an integrated model, making the application’s data flow relevant to the attack path. The work establishes a security possibility in studied systems; it does not provide a population estimate for all LLM applications. [[4]](#ref4)

Wei et al. investigate why safety-trained models may still respond to jailbreaks. They propose **Competing Objectives** [[TN3]](#term-competing-objectives) and **Mismatched Generalization** [[TN4]](#term-mismatched-generalization) as explanations and evaluate attacks on the models and requests in their study. Their analysis concerns model safety behavior and does not evaluate a PI-Guard detector. [[5]](#ref5)

Shen et al. analyze jailbreak prompts collected from online communities and evaluate their effects on language models. This work adds evidence about observed attack strategies and model responses, while its unit of analysis differs from a classifier that labels an incoming prompt before it reaches a target model. [[11]](#ref11)

### 2.2.2 Benchmarks and evaluation settings

Yi et al. introduce BIPIA to evaluate indirect prompt injection in applications that use external content. The paper studies model susceptibility and defenses in its benchmark settings; its results do not directly measure a separate PI-Guard classifier. [[23]](#ref23)

Chao et al. introduce JailbreakBench as an open benchmark with attack artifacts, a dataset of 100 behaviors, and a standardized framework for evaluating jailbreak attacks and defenses. Its focus is the behavior of language models under jailbreak attempts, rather than the project’s full input-classification and API-integration objective. [[34]](#ref34)

Jacob et al. present PromptShield as a benchmark for training and evaluating deployable prompt-injection detectors. Their benchmark includes conversational and application-structured data and examines the low false-positive-rate regime. These results support the importance of evaluating false alarms, but their performance claims remain tied to their data and protocol. [[30]](#ref30)

The benchmarks above address different questions. BIPIA studies indirect attacks through external content, JailbreakBench studies model behavior under jailbreaks, and PromptShield evaluates input detectors. Their scores should not be combined or ranked without matching the task, labels, split, model, and metric definitions. [[23]](#ref23) [[34]](#ref34) [[30]](#ref30)

### 2.2.3 Model-based detection and defenses

Meta’s Prompt Guard 86M model card describes a classifier for benign inputs, prompt injections, and jailbreaks. It recommends adapting the model to application-specific data and using model-based detection alongside other protections. This is a public model reference, not evidence that PI-Guard has the same data, checkpoint, or results. [[20]](#ref20)

Li et al. present PIGuard as a prompt-injection guardrail designed to reduce over-defense. Their paper introduces NotInject, a set of benign examples containing words that can appear in attacks, and a training strategy called Mitigating Over-defense for Free. PIGuard is a relevant injection-detection study; its results do not establish performance for the project’s registered three-label objective. [[18]](#ref18)

Liu et al. present DataSentinel, which fine-tunes a language model to detect prompt injections adapted to evade detection and formulate training as a minimax optimization problem. This provides an adversarially oriented detection approach, with a model and training setup distinct from a classical text classifier. [[32]](#ref32)

Together, Prompt Guard, PIGuard, PromptShield, and DataSentinel show that detector design includes choices about labels, training data, false alarms, and the assumed attacker. The studies provide candidate methods and evaluation lessons; none supplies PI-Guard’s local measurements. [[18]](#ref18) [[20]](#ref20) [[32]](#ref32) [[30]](#ref30)

## 2.3 Summary and Synthesis of the Literature

The reviewed research develops along three connected lines. Early prompt-injection work demonstrates direct attacks and prompt disclosure, while later work extends the attack path to external content processed by LLM applications. Jailbreak studies examine attempts to bypass model safety behavior. [[3]](#ref3) [[4]](#ref4) [[5]](#ref5) [[11]](#ref11)

Benchmark studies make these problems measurable, but each benchmark fixes its own inputs, labels, threat model, and outcome. A result about an LLM’s response to a jailbreak is different from a detector’s false-positive rate on benign prompts. A literature comparison must preserve those distinctions. [[23]](#ref23) [[34]](#ref34) [[30]](#ref30)

The literature also identifies a practical trade-off: a detector should catch malicious inputs while avoiding false alarms on legitimate text. PIGuard studies benign examples containing attack-related words, and PromptShield evaluates detectors in a low false-positive-rate regime. These findings support measuring both attack detection and benign-input errors in PI-Guard; they do not determine the project’s achieved metrics. [[18]](#ref18) [[30]](#ref30)

Across the selected studies, the research gap for PI-Guard is an evidence and integration task. The project needs to define how source datasets map to its labels, evaluate classifiers on a traceable protocol, and connect the selected classifier to the registered API guardrail. This is the project’s planned work, not a claim that existing literature lacks prompt detectors. ([Project Register](../../../../../CAPSTONE%20PROJECT%20REGISTER.md)) [[20]](#ref20) [[23]](#ref23) [[34]](#ref34) [[30]](#ref30)

## 2.4 Contribution of the Research

The project register defines four intended contributions: curate and label public prompts; compare classical and transformer classifiers; integrate a trained classifier into an API-driven guardrail; and evaluate accuracy, false-positive rates, and robustness to obfuscated or novel attacks. These are objectives whose completion must be shown in later methodology and results chapters. ([Project Register](../../../../../CAPSTONE%20PROJECT%20REGISTER.md))

Accordingly, this literature review positions PI-Guard as an applied evaluation and integration project. It does not claim a new attack taxonomy, a universally effective detector, or an achieved performance result. Any future comparison must state the dataset source, label mapping, split, model, threshold-selection procedure, metric denominator, and execution evidence.

## BẢNG THUẬT NGỮ & KHÁI NIỆM HỌC THUẬT NỀN TẢNG (ACADEMIC CONCEPT GLOSSARY)

| Mã neo | Thuật ngữ và bản dịch | Định nghĩa khoa học | Vai trò trong PI-Guard | Nguồn |
|---|---|---|---|---|
| <a id="term-goal-hijacking"></a>TN1 | Goal Hijacking (chiếm hướng mục tiêu) | An attack that redirects a model from the application’s intended task toward an attacker-selected output. | A direct prompt-injection goal considered when defining attack labels. | Perez and Ribeiro (2022). [[3]](#ref3) |
| <a id="term-prompt-leaking"></a>TN2 | Prompt Leaking (làm lộ prompt) | An attempt to make a model reveal some or all of the prompt that was supplied to guide its task. | A disclosure-oriented attack example to distinguish in the project’s label policy. | Perez and Ribeiro (2022). [[3]](#ref3) |
| <a id="term-competing-objectives"></a>TN3 | Competing Objectives (mục tiêu cạnh tranh) | A hypothesized safety-training failure in which model capabilities and safety goals conflict on a request. | A literature explanation for some jailbreak behaviors, not a detector result. | Wei et al. (2023). [[5]](#ref5) |
| <a id="term-mismatched-generalization"></a>TN4 | Mismatched Generalization (khái quát hóa không khớp) | A hypothesized failure in which safety training does not generalize to a domain where the model retains relevant capabilities. | A reason to evaluate varied attack settings, without assuming that one benchmark covers them all. | Wei et al. (2023). [[5]](#ref5) |

## References

The numeric anchors follow the local [References Log](../../../References/REFERENCES_LOG.md). Bibliographic details below identify the cited papers; local PDFs are linked for review.

<a id="ref3"></a>**[3]** Fábio Perez and Ian Ribeiro. “Ignore Previous Prompt: Attack Techniques For Language Models.” NeurIPS Workshop on Machine Learning Safety, 2022. [Local PDF](../../../References/Perez_2022_Ignore_This_Title_Hack_This_Paper_Prompt_Injection.pdf).

<a id="ref4"></a>**[4]** Kai Greshake et al. “Not What You’ve Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection.” ACM AISec, 2023. [Local PDF](../../../References/Greshake_2023_Indirect_Prompt_Injection.pdf).

<a id="ref5"></a>**[5]** Alexander Wei, Nika Haghtalab, and Jacob Steinhardt. “Jailbroken: How Does LLM Safety Training Fail?” NeurIPS 2023. [Local PDF](../../../References/Wei_2024_Jailbroken_How_LLM_Safety_Training_Fails.pdf).

<a id="ref11"></a>**[11]** Xinyue Shen et al. “Do Anything Now: Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models.” ACM CCS, 2024. [Local PDF](../../../References/Shen_2024_Do_Anything_Now_Jailbreak_Prompts_In_The_Wild.pdf).

<a id="ref18"></a>**[18]** Hao Li et al. “PIGuard: Prompt Injection Guardrail via Mitigating Over-defense for Free.” ACL, 2025. [Local PDF](../../../References/PIGuard_2025_Prompt_Injection_Guardrail_ACL.pdf).

<a id="ref20"></a>**[20]** Meta AI. “Prompt Guard 86M Model Card.” 2024. [Local model card PDF](../../../References/Meta_2024_Prompt_Guard_86M_Input_Guardrail.pdf).

<a id="ref23"></a>**[23]** Jingwei Yi et al. “Benchmarking and Defending Against Indirect Prompt Injection Attacks on Large Language Models.” KDD 2025, pp. 1809–1820. arXiv:2312.14197. [arXiv record](https://arxiv.org/abs/2312.14197) · [Local PDF](../../../References/Viet_2024_BIPIA_Benchmarking_Indirect_Prompt_Injection_Attacks.pdf).

<a id="ref32"></a>**[32]** Yupei Liu et al. “DataSentinel: A Game-Theoretic Detection of Prompt Injection Attacks.” IEEE Symposium on Security and Privacy, 2025. [Local PDF](../../../References/Liu_2025_DataSentinel_Game_Theoretic_Detection_Prompt_Injection.pdf).

<a id="ref34"></a>**[34]** Patrick Chao et al. “JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models.” NeurIPS Datasets and Benchmarks Track, 2024. [Local PDF](../../../References/Chao_2024_JailbreakBench_Open_Robustness_Benchmark_NeurIPS.pdf).

<a id="ref30"></a>**[30]** Dennis Jacob et al. “PromptShield: Deployable Detection for Prompt Injection Attacks.” CODASPY, 2025. [arXiv record](https://arxiv.org/abs/2501.15145) · [Local PDF](../../../References/Jacob_2025_PromptShield_Deployable_Detection_CODASPY.pdf).
