# EC4308 Diabetes Prediction

Replication of Islam et al. (2019) — "Likelihood Prediction of Diabetes at Early Stage Using Data Mining Techniques", ISCMM 2019.

Dataset: [UCI Early Stage Diabetes Risk Prediction](https://archive.ics.uci.edu/dataset/529) (520 records, 16 features)

## Structure

```
data/              raw dataset
src/
  zirui_models.ipynb       RF, Decision Tree, XGBoost (replication + extension)
  zirui_extensions.ipynb   SHAP, learning curves, hyperparameter tuning
figures/           generated plots
```

## How to run

```
pip install -r requirements.txt
```

Then open the notebooks in Jupyter and run all cells.
