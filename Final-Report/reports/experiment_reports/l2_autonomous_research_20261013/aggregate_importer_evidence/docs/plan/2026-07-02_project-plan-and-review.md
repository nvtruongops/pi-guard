# LLM Red-Team Corpus + Taxonomy — 정본 기획안 & 전수검토 종합

> **작성일:** 2026-07-02
> **단계:** Phase 1 Week 1 (scaffolding) 완료 직후, GATE 0 착수 전
> **문서 성격:** 프로젝트 정본 기획안 + 3-관점(긍정/부정/중립) 멀티에이전트 전수검토 종합 (Fable 5)
> **다음 버전:** GATE 0/1/2 실행 시점마다 갱신

---

## 1. 프로젝트 개요

publicly-sourced LLM red-team / safety 데이터셋을 **CC-BY-4.0 core + non-commercial extended**로
분리 통합한 **living aggregated corpus** + **cross-framework taxonomy(Phase 2)**.

- **배포 채널(주):** Hugging Face Datasets (`rubyglask/llm-redteam-corpus-taxonomy-{core,extended}`)
- **코드 리포:** https://github.com/Rubyglask/llm-redteam-corpus-taxonomy
- **저자:** rubyglask (rubyglask@gmail.com) — solo maintainer, 개인 계정 authorship
- **기원:** 원본 anvil-v8(회사 관련 red-team framework)에서 파생. **CNS zero contact** 원칙 —
  public data만 재수집, 회사 정보/점검대상 정보 절대 미포함.

## 2. 목표 & KPI

### 2.1 표면 목표 (초기)
- HF Datasets 다운로드 극대화 → "HF에서 가장 다운로드 많은 LLM red-team corpus"
- 부수: 제작자 이민(EB-1A/O-1) objective evidence

### 2.2 KPI 재프레임 (2026-07-02 검토 결과 — 중대 변경 후보)
3-관점 검토 결론: **HF downloads는 이민 evidence로서 2/5 약한 KPI** (USCIS 8-criteria에
"다운로드" 항목 없음, 봇/CI 부풀림, "재포장 aggregation은 original contribution 약함").

→ **올바른 KPI = citations + external adoption** (제3자 인용 3.5/5, 표준/제품 채택 4/5).
→ 이를 만들 유일한 차별화 자산 = **cross-mapping (Phase 2)**. GATE 2에서 Phase 순서 재검토.

## 3. 3-Phase 로드맵

| Phase | 기간 | 목표 | 완료 게이트 |
|---|---|---|---|
| **1** | 2026-Q3 (8-10주) | corpus core+extended HF 공개, arXiv preprint, Zenodo DOI, CI 자동화, evidence timeline 착수 | HF 공개 + arXiv + DOI 모두 |
| **2** | 2026-Q4 전반 (6-8주) | 7 framework taxonomy JSON + cross-mapping(~300 items) + Papers with Code 등재 | cross-mapping + PwC + external reviewer 2명 |
| **3** | 2026-Q4 후반 (4-6주) | 통합 v1.0 (corpus × taxonomy 자동 annotation) + HF Space demo + discovery event | v1.0 + Space + HN/arXiv/HF 3채널 |

Phase 1 주차 계획: W1 scaffolding(완료) → W2 소스 재수집 → W3 canonical+dedup →
W4 3-format 빌드 → W5 HF 등록 → W6 GitHub CI → W7 문서완성 → W8 arXiv+DOI →
W9 signal 인프라 → W10 buffer+게이트리뷰.

## 4. 3-관점 전수검토 종합 (2026-07-02, Fable 5 멀티에이전트)

### 4.1 관점별 핵심 명제

| 관점 | 판정 | 핵심 |
|---|---|---|
| 긍정 | 방향 옳음 | 라이선스 분리·정직한 skeleton·provenance 완성형·cross-mapping first-mover. 단일 액션: 최소 스펙이라도 HF 실게시+카운터 |
| 부정 | 차별화 2축 취약 | 16vs17 개수 모순, UnSmile 라이선스, HF 케이싱, pyproject 부재 |
| 중립 | 집계 상한 낮음 | 정본 17/13, 실코드 0줄, 이민 KPI 2/5, 경쟁 집계물 Necent 월 681 다운로드 |

### 4.2 외부 실검증 (main-loop, HF/GitHub API) — 에이전트 주장 교정

| 항목 | 에이전트 주장 | 실측 | 판정 |
|---|---|---|---|
| HF 케이싱 404 | 대소문자 구분 → load 404 | 대/소문자 둘 다 HTTP 200 | ❌ 반박 (문서 위생만) |
| HH-RLHF non-MIT | MIT 아닐 것 | HF API `license: mit` | ❌ 반박 (core 정당) |
| venv git-tracked | lint 오염 | tracked 0개 | ❌ 기우 |
| **AART 라이선스** | (놓침) | 문서 Apache-2.0 → 실측 **cc-by-4.0** | ⚠️ 문서 오류 발견 |
| **UnSmile 라이선스** | "CC-BY-SA-4.0" | github/HF 메타·README **부재** | ⚠️ 출처불명, 재배포권 불확실 |
| **Necent 집계물** | — | 30+소스 집계가 월 681 다운로드 (원본은 5K-18K) | ✅ "집계는 원본 못이김" 실증 |

### 4.3 3/3 합의 지점
1. 정본 = **17 sources / 13 core** ("16/12"는 오류)
2. 차별화 본체 = corpus 집계가 아니라 **cross-mapping(Phase 2)**
3. **실코드 0줄**이 최대 실행 리스크 (pyproject·import_all 부재)
4. **이민 evidence로서 HF downloads는 약함** (긍정도 "보조지표"로 인정)

### 4.4 최대 충돌 = 속도(긍정) vs 정확도(부정/중립)
→ 해소: **GATE 0을 HF 게시 전에 끼우면 둘 다 만족** (~1시간 정본화).

## 5. 확정 팩트 & 즉시 수정 목록 (GATE 0 대상)

| 심각도 | 항목 | 위치 | 조치 |
|---|---|---|---|
| 높음 | UnSmile 라이선스 불명 | license_matrix #13 | core에서 HOLD, 원저자 확인 전까지 pending |
| 높음 | 16→17, 12→13 개수 | README:9,21 · CITATION:17 · METHODOLOGY:18,100 · DATASET_CARD:35 | 정본화 |
| 중간 | AART Apache→CC-BY-4.0 | license_matrix #10 | 실측값 수정 |
| 중간 | ~95K/~34K 근거없음 | 전 문서 | "estimate/target" 한정어 |
| 낮음 | 케이싱 통일 | data/extended/DATASET_CARD:74 | 위생 |
| 낮음 | pyproject·import_all 부재 | ci.yml:39 등 | GATE 1 |

## 6. 직렬 게이트 (INTJ)

- **GATE 0 — 정본화** (즉시, ~1시간): 전소스 라이선스 HF API 재검증 → license_matrix 교정,
  UnSmile HOLD, 숫자 정본화, estimate 한정어. **← 현재 실행 중**
- **GATE 1 — Vertical slice**: pyproject.toml + import_all.py + build_corpus를 1개 소스(AdvBench)로
  end-to-end 관통. 검증: `pip install -e .` + canonical.parquet 1개 + verify 통과.
- **GATE 2 — KPI/Phase 순서 결정** (사용자 전략): downloads→citations 전환 여부,
  cross-mapping 앞당길지.

## 7. 이민 Evidence 전략 (재설계)

- **현 계획 무게 ≈ 2/5.** downloads는 marketing metric.
- **전환 방향:** citations + adoption 중심. cross-mapping(Phase 2)이 "no unified crosswalk exists"를
  실제로 메우면 인용·채택을 부르는 유일한 신규 지식자산.
- **유지할 강점:** 개인 authorship 강제, baseline=0 timestamp, HF 3rd-party-verifiable 수치,
  CITATION.cff 실명 + Zenodo DOI 라인.

## 8. base rate (실측, 2026-07)

| 데이터셋 | 유형 | 월 다운로드 |
|---|---|---|
| BeaverTails | 원본 | 18,275 |
| AdvBench (walledai) | 원본 | 12,131 |
| HarmBench (walledai) | 원본 | 7,136 |
| Toxic-Chat | 원본 | 5,655 |
| Necent (30+ 집계) | 집계 | 681 |

→ 이 프로젝트 현실적 상한: 24개월 중앙값 HF 150-400/월, GitHub 15-40 stars.
상향 꼬리(arXiv 인용·cross-mapping 채택) 존재하나 base rate상 희박.
**생존 가치는 "17개 모음"이 아니라 (a) 법적으로 clean한 core + (b) cross-mapping.**
