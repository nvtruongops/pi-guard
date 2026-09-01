import time
from typing import List, Callable, Dict, Any
import numpy as np

class LatencyProfiler:
    """Measures inference latency percentiles (P50, P95, P99) for guardrail classifiers."""

    @staticmethod
    def profile(
        predict_fn: Callable[[List[str]], Any],
        sample_texts: List[str],
        warmup_runs: int = 20,
        benchmark_runs: int = 100
    ) -> Dict[str, float]:
        # 1. Warmup runs
        for i in range(warmup_runs):
            sample = sample_texts[i % len(sample_texts)]
            predict_fn([sample])

        # 2. Timing benchmark
        latencies = []
        for i in range(benchmark_runs):
            sample = sample_texts[i % len(sample_texts)]
            start = time.perf_counter()
            predict_fn([sample])
            elapsed_ms = (time.perf_counter() - start) * 1000.0
            latencies.append(elapsed_ms)

        return {
            "p50_ms": float(np.percentile(latencies, 50)),
            "p95_ms": float(np.percentile(latencies, 95)),
            "p99_ms": float(np.percentile(latencies, 99)),
            "mean_ms": float(np.mean(latencies)),
            "min_ms": float(np.min(latencies)),
            "max_ms": float(np.max(latencies))
        }
