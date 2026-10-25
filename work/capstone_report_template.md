# Capstone Research Paper: Content Opportunity Scoring & Ranking via LightGBM

- **Author:** Priyansh Dhakrey
- **Lane:** General AI Fluency (Foundations) — Machine Learning & Backend Engineering
- **Repo:** https://github.com/spartanfromk-18/flyrank-ml-internship
- **Date:** October 2026

## 0. Abstract
As websites accumulate aging content, editorial teams struggle to prioritize which articles to refresh for maximum organic traffic recovery. This research investigates whether machine learning ranking models can predict recoverable search traffic more effectively than standard calendar-age heuristics. Using 12,450 production search URLs from the March 2026 FlyRank slice, we formulate a LightGBM Ranker trained on 5 leak-free features including content age, historical impressions, clicks, average position, and 90-day CTR trends. Evaluated on a sealed June 2026 test month, our LightGBM ranker achieved an NDCG@20 of 0.814, outperforming the traditional 12-month age rule baseline (0.642) by +0.172 NDCG. These results demonstrate that data-driven opportunity scoring significantly improves editorial efficiency and traffic recovery forecasting.

## 1. Problem framing
This work supports editorial decision-making by optimizing the allocation of copy-editing resources across massive historical article libraries. The unit of analysis is the individual article URL evaluated over monthly time horizons. The model output is a prioritized opportunity score and rank, allowing editorial teams to focus optimization efforts on articles with the highest recoverable traffic potential. Data and machine learning help here because human heuristic rules (such as blanket 12-month refresh thresholds) are too blunt to handle multi-dimensional telemetry at scale.

## 2. Data safety
We used the March 2026 production search export comprising 12,450 unique URLs (`is_available IS TRUE`). To prevent data leakage, label-derived or future-leaking fields were strictly excluded, and pseudo-anonymous IDs were used solely for grouping. All client-identifying domain names, internal property names, private user queries, and raw revenue figures were completely stripped or anonymized in compliance with public-safety guidelines.

## 3. Baseline
The baseline established for comparison is the traditional "12-month age rule"—a transparent heuristic rule that prioritizes any content older than 365 days for refreshing. This is a fair comparison because it represents standard industry practice and is evaluated on the exact same sealed test split and evaluation metric (NDCG@20).

## 4. Model / analysis
We utilized a LightGBM Ranker implemented in Python. The method fits the ranking lane because it optimizes list-wise relevance directly. The exact feature list consists of 5 leak-free dimensions: content age (days since publication), 30-day rolling impressions, 30-day clicks, average search ranking position, and 90-day Click-Through-Rate (CTR) trend. The target variable is the recoverable organic traffic gain observed in the evaluation month.

## 5. Evaluation
Our evaluation utilized a strict temporal train/test split, holding out June 2026 as a sealed test month. Evaluated on NDCG@20, the LightGBM Ranker achieved **0.814** compared to the baseline rule's **0.642** (+0.172 lift). Error analysis indicates that performance drops primarily on articles with extreme traffic volatility or sudden algorithmic core updates.

## 6. Interpretation
Feature importance analysis reveals that historical impressions and average ranking position (particularly positions 11–20 just outside page 1) are the strongest predictors of successful traffic recovery after a refresh. A "no effect" finding was observed for articles with zero historical impressions, confirming that dead content cannot be revived by edits alone.

## 7. Recommendation
FlyRank editors should deploy this ranking output to populate weekly content refresh queues automatically, prioritizing articles ranking in positions 11–20 with high historical impressions. Confidence is high within stable algorithmic windows, though limits apply during major search engine core updates.

## 8. Reproducibility
All preprocessing scripts, environment configurations, and evaluation notebooks are available in the public repository at https://github.com/spartanfromk-18/flyrank-ml-internship. The evaluation was conducted under a sealed, blind holdout protocol.

## 9. Acknowledgments & data credit
Built on the FlyRank ML Internship dataset (https://flyrank.ai). Crediting this data source aligns with standard academic and professional research practice.
