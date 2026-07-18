# Architecture

## Entry points

- `app.py` is the Dash application and owns presentation and callbacks.
- `build_tableau_exports.py` is a batch entry point that regenerates analytical extracts.
- `notebooks/canonical/01-severity-modeling.ipynb` is the current long-form modeling narrative.

## Modules

- `us_accidents.config` resolves external data, cache, and export locations.
- `us_accidents.features` owns deterministic feature preparation shared by batch and interactive workflows.
- `us_accidents.statistics` owns small, independently tested statistical helpers.

The application may compose these modules with Plotly, Dash, and scikit-learn, but reusable modules do not import the UI.

## Data flow

```text
external Kaggle CSV
  -> config path resolution
  -> deterministic feature preparation
  -> Dash exploration / baseline model / Tableau exports
  -> untracked caches and generated outputs
```

## Historical material

Earlier notebook versions remain in `notebooks/archive/`. They document iteration but are not equal production entry points. The canonical notebook still contains Colab-era paths in historical cells; the tested Python modules and environment-variable contract are the reproducible path forward.

