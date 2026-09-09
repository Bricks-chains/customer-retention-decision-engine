# Stage 1 - Business and data foundation

## Objective

Estimate which active customers are most likely to churn and give retention teams a ranked, explainable intervention list.

## Data contract

- One row represents one customer.
- `Churn Label` is the supervised target (`Yes`/`No`).
- Demographics, tenure, services, contract, payment method, and charges are candidate predictors.
- Raw files remain local; the repository contains code and documentation only.

## Quality and leakage decisions

Identifiers are not predictive features. `Churn Score`, `CLTV`, and `Churn Reason` are excluded from the baseline because they may be derived from the target, a post-churn process, or an existing scoring system.
