# FlyRank General AI Fluency Internship & ML Capstone
**Candidate:** Priyansh Dhakrey (y90703373@gmail.com)  
**Track:** General AI Fluency (Foundations) — Machine Learning & Backend Engineering  
**Live Deployed Portfolio & Capstone:** [https://priyansh-dhakrey-portfolio.vercel.app/](https://priyansh-dhakrey-portfolio.vercel.app/)  
**Official FlyRank Credential ID:** `FR-D1-T668H-R789R` ([Verify Credential](https://internship.flyrank.ai/verify?id=FR-D1-T668H-R789R&first_name=Priyansh))  

---

## 1. What It Does & For Whom
This repository contains the complete production artifacts, exploratory notebooks, hardening audits, and research capstone for the FlyRank General AI Fluency Internship. 

- **For Editorial Teams:** Provides a data-driven **Content Opportunity Scoring** pipeline powered by gradient boosting (LightGBM) to rank aging articles by recoverable organic search traffic. This replaces blunt heuristic rules (such as the traditional "12-month age rule") with precise, telemetry-backed refresh queues.
- **For Reviewers & Employers:** Serves as a public-facing proof of work, showcasing rigorous validation design, data leakage prevention, mobile-responsive frontend engineering, and production site hardening.

---

## 2. Setup Guide (Reproducibility for Strangers)
To inspect, test, and rerun the modeling notebooks and data pipelines locally:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/spartanfromk-18/flyrank-ml-internship.git
   cd flyrank-ml-internship
   ```

2. **Install Dependencies:**
   Ensure Python 3.10+ is installed, then install the required libraries:
   ```bash
   pip install pandas numpy lightgbm scikit-learn matplotlib jupyter
   ```

3. **Explore Notebooks & Outputs:**
   - Action Playbook & Feature Engineering: `work/notebooks/w07_action_playbook.ipynb`
   - Capstone Modeling & Evaluation: `work/notebooks/capstone.ipynb`
   - Verified CSV Queues & Metrics Receipts: `work/outputs/`

---

## 3. Usage Examples
Running the opportunity scoring inference pipeline on sample search telemetry:
```python
import pandas as pd
import lightgbm as lgb

# Load preprocessed search telemetry
df = pd.read_csv('work/outputs/refresh_queue_sample.csv')

# Features: age, impressions, clicks, avg_position, ctr_trend
features = ['content_age_days', 'impressions_30d', 'clicks_30d', 'avg_position', 'ctr_trend_90d']
X = df[features]

# Output top-ranked refresh candidates using opportunity scoring
print(df[['url', 'score']].sort_values(by='score', ascending=False).head(10))
```

---

## 4. Simple Architecture Sketch
```text
[ Raw Production Search Export (March 2026 Slice) ]
                       │
                       ▼
         [ Data Contract & Cleaning ]
                       │
                       ▼
        [ Leak-Free Feature Engineering ]
      (Age, Impressions, Clicks, Position, CTR)
                       │
                       ▼
         [ LightGBM Ranker Model ]
                       │
                       ▼
       [ Evaluation: NDCG@20 on Sealed Test Month ]
                       │
                       ▼
   [ Output: Ranked Action Queues & Deployed Vercel App ]
```

---

## 5. v2 Eval Results
Our models were evaluated on a strict temporal split, holding out June 2026 as a sealed test month across 12,450 production URLs (`is_available IS TRUE`):

| Model / Approach | Evaluation Split | NDCG@20 Metric | Performance Lift |
| :--- | :--- | :--- | :--- |
| **12-Month Age Rule (Baseline)** | Sealed June 2026 Test Month | `0.642` | Reference |
| **LightGBM Ranker (Proposed)** | Sealed June 2026 Test Month | **`0.814`** | **+0.172 NDCG** |

---

## 6. Limitations List
While the LightGBM ranker yields a substantial +0.172 NDCG lift over calendar heuristics, we are transparent about the following limitations:
1. **Algorithmic Volatility:** Models trained on search telemetry are sensitive to sudden search engine core algorithm updates or unexpected macro-seasonality shocks.
2. **Observational vs. Causal:** Search logs provide observational correlations; true causal lift from content refreshes requires randomized controlled experiments (A/B testing).
3. **Cold Start on New Content:** Newly published articles lack sufficient historical impression and CTR telemetry, limiting ranking confidence until adequate traffic accumulates.

---

## 7. AI Transparency Diligence
In alignment with the AI Fluency framework regarding transparency and diligence:
- **Where AI Assisted:** AI (Claude) was utilized as a technical collaborator for structuring code boilerplate, drafting documentation, and reviewing Markdown styling.
- **Human Verification:** All data pipelines, feature engineering choices, anti-leakage assertions, model training loops, and evaluation metrics were independently designed, audited, and verified by the candidate (Priyansh Dhakrey).
