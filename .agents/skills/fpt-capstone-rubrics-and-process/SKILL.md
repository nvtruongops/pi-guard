---
name: fpt-capstone-rubrics-and-process
description: >-
  FPT University Capstone Project (IAP491) timeline, milestone management, weekly process tracking (PROCESS_REPORT.xlsx),
  continuous assessment rubrics (Reports 1-6), and committee defense preparation.
---

# FPT University Capstone Project Process & Rubrics Guide

This skill manages project governance, weekly milestones, supervisor reporting, and grading rubrics for FPT University Capstone Projects (IAP491 Information Assurance).

> 📚 **Internal Guidelines Reference (Confidential, Local Only)**: [`docs/fpt_capstone_guide/IAP491_CP_StudentsGuideForm for Research Based Thesis.docx`](file:///d:/Work/Do-an/docs/fpt_capstone_guide/IAP491_CP_StudentsGuideForm%20for%20Research%20Based%20Thesis.docx)  
> 📑 **Official Synthesized Rubrics & Chapter Outline**: [`Final-Report/thesis/FPT_IAP491_Capstone_Guidelines_and_Rubrics_Summary.md`](file:///d:/Work/Do-an/Final-Report/thesis/FPT_IAP491_Capstone_Guidelines_and_Rubrics_Summary.md)  
> 📊 **Official Semester Process Report**: [`Final-Report/reports/PI_GUARD_PROCESS_REPORT.xlsx`](file:///d:/Work/Do-an/Final-Report/reports/PI_GUARD_PROCESS_REPORT.xlsx)  
> ⚠️ **Fall 2026 Timeline Notice**: The 15-week milestone timeline below is established specifically for the **Fall 2026 semester** in agreement with Supervisor **Trần Văn Ninh**, and is **NOT** taken from the legacy schedules stored in `docs/fpt_capstone_guide/`.

---

## 1. Grading Formula & Assessment Weights

$$\text{Final Project Mark} = (\text{Process Mark } [6 \text{ Reports}] \times 50\%) + (\text{Presentation Mark } [\text{Committee}] \times 50\%)$$

### Process Mark Weights (Continuous Assessment by Supervisor):
1. **Report No.1: Introduction** — **10%** (Due: Week 3)
2. **Report No.2: Literature Review** — **25%** (Due: Week 4)
3. **Report No.3: Methodology** — **20%** (Due: Week 7-8)
4. **Report No.4: Experimental and Results** — **25%** (Due: Week 9-11)
5. **Report No.5: Discussion** — **15%** (Due: Week 13-14)
6. **Report No.6: Conclusion and Future Work** — **5%** (Due: Week 13-14)

---

## 2. Milestone Calendar (Official Fall 2026 15-Week Timeline)

| Milestone / Week | Deliverable / Task | Assessment Focus |
| :--- | :--- | :--- |
| **Sprint Tiền Đề** | Khởi động nhóm & Duyệt đề tài | Supervisor approval on [`CAPSTONE PROJECT REGISTER.md`](file:///d:/Work/Do-an/CAPSTONE%20PROJECT%20REGISTER.md) |
| **Week 3-4** | 🎯 **REVIEW 1 (GVHD)**: Problem Definition & Lit Review | Báo cáo toàn diện **Chapter 1 (Intro - 10%) & Chapter 2 (Lit Review - 25%)** (Threat Model NIST, SOTA, 3 RQs, 4 Demo) |
| **Week 7-8** | 🎯 **REVIEW 2 (GVHD - Tuần 8)**: Methodology, Baseline ML & Cập nhật Docs | Báo cáo **Chapter 3 (Methodology - 20%)** (Dataset curation, Group-Aware Split, TF-IDF + Baseline ML results) |
| **Week 11-13** | 🏛️ **BÁO CÁO HỘI ĐỒNG 1 (Hội đồng Giữa kỳ)** | Báo cáo **Chapter 4 (Experimental and Results - 25%)** (DeBERTa-v3 Fine-tuning, ONNX INT8, FastAPI Prototype & Streamlit Demo) |
| **Week 14** | Submit **Report No.5** (Discussion - 15%) & **Report No.6** (Conclusion - 5%) | Đánh giá bảo mật, Trade-off FPR, Limitations, Future work; Quét Turnitin (< 20%), Duyệt toàn văn |
| **Week 15** | 🎓 **BÁO CÁO HỘI ĐỒNG FINAL (Bảo vệ Tốt nghiệp)** | Thuyết trình bảo vệ toàn diện 6 Chương trước Hội đồng chấm Tốt nghiệp chính thức (**50% Presentation**) |


---

## 3. Team Member Role Responsibilities (FPT IAP491)

| Student | Role | Core Technical Module | Assigned Process Reports |
| :--- | :--- | :--- | :--- |
| **Nguyễn Văn Trường (Leader)** | Architecture & Data Engineering | `Final-Report/scripts/download_dataset.py`, `Final-Report/src/datasets/splitter.py` | **Report No.1** + **Report No.2** |
| **Nguyễn Quí Đức** | Classical ML Baseline | `Final-Report/scripts/train.py`, `Final-Report/notebooks/02_baseline.ipynb` | **Report No.3** |
| **Phạm Minh Hoàng Việt** | Transformer & Robustness | `Final-Report/notebooks/03_transformer_training.ipynb`, `Final-Report/src/preprocessing/obfuscation.py` | **Report No.4** |
| **Đỗ Đoàn Duy Phương** | API Middleware & Dashboard | `Final-Report/src/api/`, `Final-Report/src/dashboard/`, Thesis Compilation | **Report No.5** + **Report No.6** |
