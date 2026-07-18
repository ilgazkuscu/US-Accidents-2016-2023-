# Dataset contract

The project uses the [U.S. Accidents dataset](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents) assembled by Sobhan Moosavi and collaborators. The accompanying paper is preserved in `reports/moosavi-us-accidents-paper.pdf` for research context.

Raw data is not committed. Download a compatible CSV and set:

```bash
export US_ACCIDENTS_CSV=/absolute/path/to/US_Accidents_March23.csv
```

The application also checks the standard `kagglehub` cache for dataset version 13 when the environment variable is absent.

Generated caches and Tableau extracts are ignored because they can be recreated. Dataset updates may change row counts and results, so record the Kaggle version and download date in any published analysis.

