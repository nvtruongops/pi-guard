---
name: ml-classifier-training
description: >-
  Training and optimization workflows for Classical ML baselines (TF-IDF + LogisticRegression / LinearSVC / XGBoost)
  and Transformer Fine-Tuning (DeBERTa-v3 / RoBERTa / BERT) for the PI-Guard Capstone Project.
---

# ML & Transformer Classifier Training Guide

This skill guides **Student 2** (Classical ML Baseline) and **Student 3** (Fine-tuned Transformer) in training, tuning, and optimizing classifiers for Prompt Injection & Jailbreak detection.

---

## 1. Classical ML Baseline (Student 2)

The baseline model must be fast, lightweight, and serve as an empirical performance benchmark.

### Recommended Pipeline: Hybrid Word + Char n-gram TF-IDF
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, roc_auc_score
import joblib

def build_baseline_pipeline():
    # Combine word and character n-grams to catch obfuscation
    word_vectorizer = TfidfVectorizer(
        ngram_range=(1, 3),
        max_features=20000,
        sublinear_tf=True
    )
    char_vectorizer = TfidfVectorizer(
        analyzer='char_wb',
        ngram_range=(3, 5),
        max_features=30000,
        sublinear_tf=True
    )
    
    features = FeatureUnion([
        ('word_tfidf', word_vectorizer),
        ('char_tfidf', char_vectorizer)
    ])
    
    # Model: LogisticRegression or LinearSVC
    pipeline = Pipeline([
        ('features', features),
        ('classifier', LogisticRegression(C=2.0, max_iter=1000, class_weight='balanced'))
    ])
    return pipeline

def train_and_save_baseline(train_df, val_df, model_save_path="models/baseline_tfidf.joblib"):
    pipeline = build_baseline_pipeline()
    pipeline.fit(train_df['text'], train_df['label'])
    
    val_preds = pipeline.predict(val_df['text'])
    print(classification_report(val_df['label'], val_preds))
    
    joblib.dump(pipeline, model_save_path)
    print(f"Baseline model saved to {model_save_path}")
```

---

## 2. Transformer Fine-Tuning (Student 3)

The primary state-of-the-art model is based on **DeBERTa-v3** due to its disentangled attention mechanism, which excels at NLP syntax and semantic boundary detection.

### Recommended Models:
- `microsoft/deberta-v3-base` (High accuracy, primary research target)
- `microsoft/deberta-v3-small` (Low latency, ideal for real-time guardrail API)
- `roberta-base` (Comparison baseline)

### Training Script with Hugging Face `Trainer`:
```python
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    DataCollatorWithPadding
)
import evaluate
import numpy as np

def compute_metrics(eval_pred):
    accuracy_metric = evaluate.load("accuracy")
    precision_metric = evaluate.load("precision")
    recall_metric = evaluate.load("recall")
    f1_metric = evaluate.load("f1")
    
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    
    acc = accuracy_metric.compute(predictions=predictions, references=labels)["accuracy"]
    prec = precision_metric.compute(predictions=predictions, references=labels)["precision"]
    rec = recall_metric.compute(predictions=predictions, references=labels)["recall"]
    f1 = f1_metric.compute(predictions=predictions, references=labels)["f1"]
    
    return {"accuracy": acc, "precision": prec, "recall": rec, "f1": f1}

def train_transformer(train_dataset, val_dataset, model_name="microsoft/deberta-v3-base", output_dir="models/deberta_guardrail"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
    
    training_args = TrainingArguments(
        output_dir=output_dir,
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=32,
        num_train_epochs=4,
        weight_decay=0.01,
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        fp16=torch.cuda.is_available(),
        logging_dir=f"{output_dir}/logs",
        logging_steps=50,
        report_to="none"
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        tokenizer=tokenizer,
        data_collator=DataCollatorWithPadding(tokenizer=tokenizer),
        compute_metrics=compute_metrics
    )
    
    trainer.train()
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    print(f"Transformer model saved to {output_dir}")
```

---

## 3. Latency Optimization (ONNX / Quantization)

For production deployment in the guardrail API:
1. Export model to ONNX runtime format.
2. Apply Dynamic INT8 Quantization (reduces model size by 4x and latency by ~2-3x with <0.5% accuracy loss).
