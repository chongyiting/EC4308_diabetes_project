# EC4308 Diabetes Prediction Project

Replication and extension of:

> Islam, M. F., Ferdousi, R., Rahman, S., & Bushra, H. Y. (2019). *Likelihood Prediction of Diabetes at Early Stage Using Data Mining Techniques.* In Computer Vision and Machine Intelligence in Medical Image Analysis: International Symposium, ISCMM 2019 (pp. 113-125). Springer Singapore.

## Project Structure

```
EC4308_diabetes_project/
├── data/
│   └── diabetes_data_clean.csv   # UCI Early Stage Diabetes dataset (520 records)
├── src/
│   └── zirui_models.py           # Random Forest, Decision Tree, XGBoost
├── figures/                      # Generated plots
│   ├── rf_feature_importance.png
│   ├── importance_matrix_heatmap.png
│   ├── decision_tree_plot.png
│   ├── xgb_feature_importance.png
│   └── roc_comparison.png
├── requirements.txt
├── .gitignore
└── README.md
```

## Models (Zirui)

| Model | Type | Description |
|-------|------|-------------|
| Random Forest | Paper Replication | RF classifier with Gini feature importance |
| Decision Tree | Paper Replication | DT classifier with tree visualization |
| XGBoost | Extension | Gradient boosting as additional benchmark |

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
python src/zirui_models.py
```

Outputs metrics (accuracy, precision, recall, F1, AUC) for both 80/20 split and 10-fold CV, plus saves all figures to `figures/`.

## Dataset

- **Source:** [UCI ML Repository - Early Stage Diabetes Risk Prediction](https://archive.ics.uci.edu/dataset/529)
- **Records:** 520 patients from Sylhet Diabetes Hospital, Bangladesh
- **Features:** 16 (age, gender, 14 binary symptoms)
- **Target:** Diabetes class (positive/negative)
