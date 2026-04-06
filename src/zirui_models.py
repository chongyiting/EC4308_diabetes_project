"""
EC4308 Final Project - Zirui's Models
Replication of: Islam et al. (2019) "Likelihood Prediction of Diabetes at Early Stage
Using Data Mining Techniques"

Models:
1. Random Forest (Paper Replication) + Feature Importance Matrix
2. Decision Tree (Paper Replication)
3. XGBoost (Extension)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import (
    train_test_split,
    StratifiedKFold,
    cross_val_score,
    cross_val_predict,
)
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
    roc_curve,
)
from xgboost import XGBClassifier

import os
import warnings
warnings.filterwarnings("ignore")

# Resolve paths relative to project root (one level up from src/)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
FIG_DIR = os.path.join(PROJECT_ROOT, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

# ============================================================
# 0. Load Data
# ============================================================
df = pd.read_csv(os.path.join(DATA_DIR, "diabetes_data_clean.csv"))
print("Dataset shape:", df.shape)
print("\nTarget distribution:")
print(df["diabetes_class"].value_counts())
print()

feature_names = [c for c in df.columns if c != "diabetes_class"]
X = df[feature_names].values
y = df["diabetes_class"].values

# Paper uses 80/20 split (percentage split) and 10-fold CV
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)
cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

print(f"Train size: {X_train.shape[0]}, Test size: {X_test.shape[0]}")
print("=" * 70)


# ============================================================
# Helper: evaluate and print metrics
# ============================================================
def evaluate_model(model, name, X_tr, y_tr, X_te, y_te, cv):
    """Fit model, print metrics for both percentage-split and 10-fold CV."""
    model.fit(X_tr, y_tr)
    y_pred = model.predict(X_te)
    y_prob = model.predict_proba(X_te)[:, 1]

    acc = accuracy_score(y_te, y_pred)
    prec = precision_score(y_te, y_pred)
    rec = recall_score(y_te, y_pred)
    f1 = f1_score(y_te, y_pred)
    auc = roc_auc_score(y_te, y_prob)
    cm = confusion_matrix(y_te, y_pred)

    print(f"\n{'=' * 70}")
    print(f" {name}")
    print(f"{'=' * 70}")

    # --- Percentage Split (80/20) ---
    print(f"\n--- 80/20 Percentage Split ---")
    print(f"  Accuracy:  {acc:.4f}")
    print(f"  Precision: {prec:.4f}")
    print(f"  Recall:    {rec:.4f}")
    print(f"  F1-Score:  {f1:.4f}")
    print(f"  AUC:       {auc:.4f}")
    print(f"\n  Confusion Matrix:")
    print(f"    {cm}")
    print(f"\n  Classification Report:")
    print(classification_report(y_te, y_pred, target_names=["Negative", "Positive"]))

    # --- 10-Fold Cross-Validation ---
    cv_acc = cross_val_score(model, np.vstack([X_tr, X_te]), np.hstack([y_tr, y_te]),
                             cv=cv, scoring="accuracy")
    cv_prec = cross_val_score(model, np.vstack([X_tr, X_te]), np.hstack([y_tr, y_te]),
                              cv=cv, scoring="precision")
    cv_rec = cross_val_score(model, np.vstack([X_tr, X_te]), np.hstack([y_tr, y_te]),
                             cv=cv, scoring="recall")
    cv_f1 = cross_val_score(model, np.vstack([X_tr, X_te]), np.hstack([y_tr, y_te]),
                            cv=cv, scoring="f1")
    cv_auc = cross_val_score(model, np.vstack([X_tr, X_te]), np.hstack([y_tr, y_te]),
                             cv=cv, scoring="roc_auc")

    print(f"--- 10-Fold Cross-Validation ---")
    print(f"  Accuracy:  {cv_acc.mean():.4f} (+/- {cv_acc.std():.4f})")
    print(f"  Precision: {cv_prec.mean():.4f} (+/- {cv_prec.std():.4f})")
    print(f"  Recall:    {cv_rec.mean():.4f} (+/- {cv_rec.std():.4f})")
    print(f"  F1-Score:  {cv_f1.mean():.4f} (+/- {cv_f1.std():.4f})")
    print(f"  AUC:       {cv_auc.mean():.4f} (+/- {cv_auc.std():.4f})")

    return model, y_pred, y_prob


# ============================================================
# 1. Random Forest (Paper Replication)
# ============================================================
rf = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
)
rf_model, rf_pred, rf_prob = evaluate_model(
    rf, "Random Forest (Paper Replication)", X_train, y_train, X_test, y_test, cv
)

# --- Feature Importance Matrix ---
importances = rf_model.feature_importances_
indices = np.argsort(importances)[::-1]

print("\n--- Random Forest Feature Importance Ranking ---")
for rank, idx in enumerate(indices, 1):
    print(f"  {rank:2d}. {feature_names[idx]:25s}  {importances[idx]:.4f}")

# Plot feature importance
fig, ax = plt.subplots(figsize=(10, 6))
sorted_idx = np.argsort(importances)
ax.barh(
    [feature_names[i] for i in sorted_idx],
    importances[sorted_idx],
    color="steelblue",
)
ax.set_xlabel("Feature Importance (Gini)")
ax.set_title("Random Forest — Feature Importance")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "rf_feature_importance.png"), dpi=150)
plt.close()
print("\n  [Saved: rf_feature_importance.png]")

# Correlation-based importance heatmap (importance matrix)
fig, ax = plt.subplots(figsize=(12, 10))
corr = df[feature_names + ["diabetes_class"]].corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0, ax=ax)
ax.set_title("Feature Correlation Matrix (Importance Matrix)")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "importance_matrix_heatmap.png"), dpi=150)
plt.close()
print("  [Saved: importance_matrix_heatmap.png]")


# ============================================================
# 2. Decision Tree (Paper Replication)
# ============================================================
dt = DecisionTreeClassifier(
    random_state=42,
)
dt_model, dt_pred, dt_prob = evaluate_model(
    dt, "Decision Tree (Paper Replication)", X_train, y_train, X_test, y_test, cv
)

# Plot decision tree (limited depth for readability)
fig, ax = plt.subplots(figsize=(24, 12))
plot_tree(
    dt_model,
    feature_names=feature_names,
    class_names=["Negative", "Positive"],
    filled=True,
    rounded=True,
    max_depth=4,
    fontsize=8,
    ax=ax,
)
ax.set_title("Decision Tree (max_depth=4 for visualization)")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "decision_tree_plot.png"), dpi=150)
plt.close()
print("\n  [Saved: decision_tree_plot.png]")


# ============================================================
# 3. XGBoost (Extension beyond paper)
# ============================================================
xgb = XGBClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=6,
    random_state=42,
    use_label_encoder=False,
    eval_metric="logloss",
)
xgb_model, xgb_pred, xgb_prob = evaluate_model(
    xgb, "XGBoost", X_train, y_train, X_test, y_test, cv
)

# XGBoost feature importance
xgb_imp = xgb_model.feature_importances_
xgb_sorted = np.argsort(xgb_imp)
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(
    [feature_names[i] for i in xgb_sorted],
    xgb_imp[xgb_sorted],
    color="darkorange",
)
ax.set_xlabel("Feature Importance (Gain)")
ax.set_title("XGBoost — Feature Importance")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "xgb_feature_importance.png"), dpi=150)
plt.close()
print("\n  [Saved: xgb_feature_importance.png]")


# ============================================================
# 4. Comparison: ROC Curves
# ============================================================
fig, ax = plt.subplots(figsize=(8, 6))
for name, y_p in [("Random Forest", rf_prob), ("Decision Tree", dt_prob), ("XGBoost", xgb_prob)]:
    fpr, tpr, _ = roc_curve(y_test, y_p)
    auc_val = roc_auc_score(y_test, y_p)
    ax.plot(fpr, tpr, label=f"{name} (AUC={auc_val:.3f})")

ax.plot([0, 1], [0, 1], "k--", alpha=0.4)
ax.set_xlabel("False Positive Rate")
ax.set_ylabel("True Positive Rate")
ax.set_title("ROC Curve Comparison")
ax.legend(loc="lower right")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "roc_comparison.png"), dpi=150)
plt.close()
print("\n[Saved: roc_comparison.png]")


# ============================================================
# 5. Summary Table
# ============================================================
print("\n" + "=" * 70)
print(" SUMMARY — 80/20 Percentage Split Results")
print("=" * 70)

summary = []
for name, pred, prob in [
    ("Random Forest", rf_pred, rf_prob),
    ("Decision Tree", dt_pred, dt_prob),
    ("XGBoost", xgb_pred, xgb_prob),
]:
    summary.append({
        "Model": name,
        "Accuracy": accuracy_score(y_test, pred),
        "Precision": precision_score(y_test, pred),
        "Recall": recall_score(y_test, pred),
        "F1-Score": f1_score(y_test, pred),
        "AUC": roc_auc_score(y_test, prob),
    })

summary_df = pd.DataFrame(summary)
summary_df = summary_df.set_index("Model")
print(summary_df.round(4).to_string())
print(f"\nDone. All plots saved to {FIG_DIR}")
