# Stage 4 - Decision engine

Predictions become useful only when connected to an action. The engine calculates:

`expected value at risk = churn probability x monthly value`

`net retention value = expected value at risk - contact cost`

It assigns three transparent tiers: Monitor, Proactive outreach, and Priority save. In production, tiers should be calibrated against uplift experiments and constrained by contact capacity, consent, fairness review, and offer eligibility.
