# U.S. Accident Severity Analysis

A reproducible analysis scaffold and Dash exploration app for the U.S. Accidents dataset. The project studies severity, weather, time, geography, and road context while keeping post-event leakage risks explicit.

## Repository map

```text
app.py                         Dash application entry point
src/us_accidents/              Reusable configuration, features, and statistics
notebooks/canonical/           Current modeling narrative
notebooks/archive/             Earlier notebook iterations, preserved for history
tests/                         Synthetic-data unit tests
data/README.md                 Dataset contract and acquisition
reports/                       Source paper and project presentation
docs/architecture.md           Runtime and module boundaries
build_tableau_exports.py       Regenerates untracked Tableau extracts
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

Download the dataset as described in `data/README.md`, then set:

```bash
export US_ACCIDENTS_CSV=/absolute/path/to/US_Accidents_March23.csv
```

Run the application:

```bash
python app.py
```

Generate Tableau extracts:

```bash
python build_tableau_exports.py
```

## Validation

```bash
pytest
ruff check src tests app.py build_tableau_exports.py
```

## Modeling boundaries

- `Severity >= 3` is treated as the severe class in the current baseline.
- Post-event extent fields such as `Distance(mi)` are excluded from the baseline feature set.
- Random train/test splitting does not prove future or geographic generalization. A production study should use temporal and geographic holdouts.
- The repository does not claim causal effects or production-ready road-risk predictions.

