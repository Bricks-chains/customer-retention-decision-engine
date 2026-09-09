# Stage 3 - Predictive modeling

Start with a class-weighted logistic-regression baseline. The `ColumnTransformer` keeps numeric imputation/scaling and categorical one-hot encoding inside a single pipeline, preventing train/test leakage.

Use a stratified holdout and report ROC-AUC, PR-AUC, recall at an operational threshold, and calibration. The model should be compared with a simple majority-class baseline before any tuning.
