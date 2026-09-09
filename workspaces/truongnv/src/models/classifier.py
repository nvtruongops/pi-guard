import os
import re
from abc import ABC, abstractmethod

import joblib
import numpy as np


class BaseGuardrailClassifier(ABC):
    """Abstract base class for all Guardrail classifiers."""

    @abstractmethod
    def predict_score(self, texts: str | list[str]) -> list[float]:
        """Returns the probability score (0.0 to 1.0) of being malicious for each input text."""
        pass

    @abstractmethod
    def load(self, path: str) -> None:
        """Loads model weights from disk."""
        pass


class TfidfBaselineClassifier(BaseGuardrailClassifier):
    """Classical ML baseline combining character and word n-grams with a linear classifier."""

    def __init__(self, model_path: str = None):
        self.model = None
        if model_path and os.path.exists(model_path):
            self.load(model_path)

    def load(self, path: str) -> None:
        self.model = joblib.load(path)

    def predict_score(self, texts: str | list[str]) -> list[float]:
        if isinstance(texts, str):
            texts = [texts]
        if self.model is None:
            return [0.05 for _ in texts]

        if hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba(texts)
            return [float(p[1]) for p in probs]
        elif hasattr(self.model, "decision_function"):
            decision = self.model.decision_function(texts)
            return [float(1.0 / (1.0 + np.exp(-d))) for d in decision]
        else:
            preds = self.model.predict(texts)
            return [float(p) for p in preds]


class DummyClassifier(BaseGuardrailClassifier):
    """Fast dummy classifier for testing, CI pipelines, and unit tests."""

    def __init__(self, default_score: float = 0.10):
        self.default_score = default_score

    def load(self, path: str) -> None:
        pass

    def predict_score(self, texts: str | list[str]) -> list[float]:
        if isinstance(texts, str):
            texts = [texts]
        scores = []
        attack_patterns = [
            r"ignore\s+(all\s+)?previous",
            r"disregard\s+(all\s+)?instructions",
            r"dan\s+mode",
            r"jailbreak",
            r"system\s+prompt"
        ]
        for text in texts:
            lower_text = text.lower()
            if any(re.search(pat, lower_text) for pat in attack_patterns):
                scores.append(0.95)
            else:
                scores.append(self.default_score)
        return scores
