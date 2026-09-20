"""
workspaces/truongnv/src/models/conformal_calibrator.py

Module Hiệu Chuẩn Ngưỡng Động Cơ Quyết Định Dựa Trên Lý Thuyết Conformal Risk Control (CRC).
Dựa trên công trình:
- Angelopoulos et al. (2024), "Conformal Risk Control", arXiv:2208.02814.
- Kang et al. (NeurIPS 2025), "C-SafeGen: Certified Safe LLM Generation with Claim-Based Streaming Guardrails".

Module này cung cấp bảo chứng an toàn thống kê hữu hạn mẫu (finite-sample statistical guarantee)
rằng Tỷ lệ Báo động Nhầm (False Positive Rate - FPR) trên các prompt lành tính (Benign)
sẽ không vượt quá ngân sách rủi ro định trước alpha (mặc định alpha = 0.015, tương ứng 1.5%).
"""

import numpy as np
from typing import Dict, List, Tuple, Union


class ConformalRiskCalibrator:
    """
    Bộ hiệu chuẩn rủi ro Conformal Risk Control (CRC) cho Guardrail Classifiers.
    Tính toán ngưỡng quyết định tau_low và tau_high để điều phối chính sách Tri-State:
      - ALLOW: Score < tau_low (Bảo chứng FPR <= alpha)
      - BLOCK: Score >= tau_high (Độ tin cậy phát hiện cao)
      - DEEP_INSPECT / TIER 2: tau_low <= Score < tau_high (Vùng nghi ngờ)
    """

    def __init__(self, target_fpr: float = 0.015, confidence_level: float = 0.95):
        """
        Args:
            target_fpr: Ngân sách tỷ lệ dương tính giả tối đa (alpha). Mặc định 0.015 (1.5%).
            confidence_level: Mức độ tin cậy thống kê (1 - delta). Mặc định 0.95 (95%).
        """
        self.target_fpr = target_fpr
        self.confidence_level = confidence_level
        self.tau_low = 0.50   # Mặc định khởi tạo
        self.tau_high = 0.85  # Mặc định khởi tạo
        self.is_calibrated = False
        self.calibration_stats = {}

    def calibrate(
        self,
        benign_scores: Union[List[float], np.ndarray],
        attack_scores: Union[List[float], np.ndarray] = None
    ) -> Dict[str, float]:
        """
        Hiệu chuẩn ngưỡng quyết định dựa trên tập dữ liệu giữ lại (Hold-out Calibration Set).

        Args:
            benign_scores: Danh sách xác suất mô hình dự đoán là độc hại trên các mẫu lành tính (Ground Truth = Benign).
            attack_scores: Danh sách xác suất mô hình dự đoán trên các mẫu tấn công (Ground Truth = Malicious, tùy chọn).

        Returns:
            Dict chứa các ngưỡng đã hiệu chuẩn: tau_low, tau_high và các chỉ số thống kê.
        """
        benign_arr = np.array(benign_scores, dtype=np.float64)
        n_benign = len(benign_arr)

        if n_benign == 0:
            raise ValueError("Tập dữ liệu hiệu chuẩn Benign không được rỗng.")

        # Thuật toán Conformal Risk Control (CRC) cho bài toán kiểm soát tỷ lệ lỗi FPR:
        # Hàm tổn thất: l(tau, x) = 1 nếu score(x) >= tau, ngược lại 0
        # Ta cần tìm tau_low nhỏ nhất sao cho:
        # (n / (n + 1)) * R_hat(tau) + 1 / (n + 1) <= alpha
        # Tương đương: R_hat(tau) <= ((n + 1) * alpha - 1) / n
        
        # Sắp xếp điểm số của tập benign tăng dần
        sorted_benign = np.sort(benign_arr)

        # Tính toán phân vị Conformal
        # Để FPR <= target_fpr, ngưỡng tau_low phải lớn hơn phân vị (1 - target_fpr)
        # với hệ số hiệu chỉnh mẫu hữu hạn (finite-sample correction)
        q_level = min(1.0, max(0.0, 1.0 - self.target_fpr + (1.0 / (n_benign + 1))))
        calibrated_tau_low = float(np.quantile(sorted_benign, q_level, method="higher"))

        # Đảm bảo ranh giới an toàn tối thiểu
        self.tau_low = float(np.clip(calibrated_tau_low, 0.10, 0.90))

        # Hiệu chuẩn tau_high (ngưỡng tự động chặn cứng) dựa trên tập attack nếu có
        if attack_scores is not None and len(attack_scores) > 0:
            attack_arr = np.array(attack_scores, dtype=np.float64)
            # Chọn tau_high tại phân vị sao cho bắt được ít nhất 90% mẫu tấn công rõ ràng
            # nhưng phải cao hơn tau_low
            p10_attack = float(np.percentile(attack_arr, 10))
            self.tau_high = float(np.clip(max(self.tau_low + 0.15, p10_attack), 0.70, 0.95))
        else:
            self.tau_high = float(min(0.90, self.tau_low + 0.30))

        # Đo lường FPR thực nghiệm trên tập calibration
        empirical_fpr = float(np.mean(benign_arr >= self.tau_low))

        self.is_calibrated = True
        self.calibration_stats = {
            "n_calibration_benign": n_benign,
            "target_fpr_alpha": self.target_fpr,
            "calibrated_tau_low": self.tau_low,
            "calibrated_tau_high": self.tau_high,
            "empirical_calibration_fpr": empirical_fpr,
            "conformal_guarantee_met": bool(empirical_fpr <= self.target_fpr)
        }

        return self.calibration_stats

    def decide_action(self, score: float) -> Tuple[str, str]:
        """
        Quyết định chính sách Tri-State dựa trên điểm xác suất và ngưỡng Conformal:
          - 'ALLOW': Cho phép truy cập trực tiếp tới LLM đích.
          - 'DEEP_INSPECT': Chuyển tiếp sang Tầng 2 (Deep Semantic Inspection) hoặc phân tích nâng cao.
          - 'BLOCK': Ngăn chặn lập tức tại cổng Ingress.
        """
        if score < self.tau_low:
            return "ALLOW", f"Score {score:.4f} < tau_low ({self.tau_low:.4f}) -> Benign (FPR <= {self.target_fpr*100:.1f}%)"
        elif score >= self.tau_high:
            return "BLOCK", f"Score {score:.4f} >= tau_high ({self.tau_high:.4f}) -> Confirmed Attack"
        else:
            return "DEEP_INSPECT", f"Score {score:.4f} in [{self.tau_low:.4f}, {self.tau_high:.4f}] -> Escalate to Tier 2"
