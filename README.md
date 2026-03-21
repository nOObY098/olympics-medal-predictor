# Olympics 2028 Medal Predictor

Predicting gold, silver, and bronze medal counts for the 2028 Los Angeles Olympics using historical data, with a focus on **home field advantage** and **economic factors**.

---

## Results

| Metric | Score |
|--------|-------|
| MAE (medals per country) | 9.35 |
| Spearman rank correlation | 0.894 |

> Key finding: Home field advantage adds ~8 medals for the USA. However, past performance (rolling 3-game average) is the strongest predictor — dominating over GDP and home advantage combined. Predictions for smaller nations are less reliable due to limited historical data.

---

## Live Demo

[Olympics 2028 Medal Predictor →](https://olympics-medal-predictor.streamlit.app/)

---

## Project Structure

```
olympics-medal-predictor/
│
├── data/
│   ├── raw/                  # Original downloaded datasets (do not edit)
│   └── processed/            # Cleaned, merged, feature-engineered data
│
├── notebooks/
│   └── olympics_predictor.ipynb   # Main analysis notebook (READ THIS FIRST)
│
├── src/
│   ├── features.py           # Feature engineering functions
│   ├── model.py              # Model training and evaluation
│   └── predict.py            # Generate 2028 predictions
│
├── app/
│   └── streamlit_app.py      # Interactive dashboard
│
├── NOTES.md                  # Raw session notes (personal log)
└── requirements.txt
```

---

## Methodology

### Data Sources
- **Medal history**: [Kaggle — 120 Years of Olympic History](https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results) — athlete-level results from 1896 to 2016, filtered to Summer Olympics only
- **Economic data**: [World Bank GDP per capita (1960–2024)](https://data.worldbank.org/indicator/NY.GDP.PCAP.CD?end=2024&start=1960&view=map&year=1960), reshaped from wide to long format and merged on country-year

### Key Features Engineered

| Feature | Description |
|---|---|
| `is_host` | Binary flag — 1 if the country is hosting that year |
| `rolling_3game_avg` | Average medals over the last 3 Olympics (shift(1) to prevent leakage) |
| `gdp_per_capita` | World Bank GDP per capita — proxy for sport investment capacity |
| `trend_slope` | Linear slope of medal counts over last 4 games — captures improving/declining nations |

GDP coverage was 64% after mapping NOC codes to World Bank ISO-3 codes. Missing values are mostly small nations with few medals — large medallist countries (USA, CHN, RUS, GBR) are fully covered.

### Model

- **Baseline**: Poisson regression — natural fit for count data (non-negative integers)
- **Final model**: XGBoost regressor (n_estimators=200, max_depth=4, learning_rate=0.05)
- **Validation**: Time-series split — train on 1960–2012, test on Rio 2016
- **Explainability**: SHAP values used to interpret feature importance per prediction

### Top 2028 Predictions

| Rank | Country | Predicted medals |
|------|---------|-----------------|
| 1 | USA | 254 |
| 2 | RUS | 162 |
| 3 | CHN | 141 |
| 4 | GBR | 117 |
| 5 | AUS | 111 |
| 6 | GER | 107 |
| 7 | FRA | 81 |
| 8 | JPN | 73 |
| 18 | CRO | 29 |

---

## How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the full analysis
jupyter notebook notebooks/olympics_predictor.ipynb

# 3. Launch the dashboard
python -m streamlit run app/streamlit_app.py
```

---

## Challenges & Decisions

- **Country name standardisation**: Kaggle uses NOC codes (e.g. `GER`), World Bank uses ISO-3 (e.g. `DEU`). Resolved by building a 150+ country mapping dictionary in `src/features.py`. Historical nations (USSR → RUS, GDR → DEU) mapped to successor states.
- **Winter Olympics filtering**: Dataset included both Summer and Winter games. Filtered to Summer only since 2028 LA is a Summer Olympics.
- **Python 3.14 compatibility**: Streamlit Cloud required Python 3.11 due to altair/pillow dependency conflicts with 3.14.
- **Data leakage prevention**: Rolling averages use `shift(1)` to ensure only past games inform each prediction. Time-series cross-validation used instead of random splits.

---

## What I Learned

- Past performance dominates over economic factors — a country's rolling medal average is a stronger predictor than GDP per capita. Wealthy nations don't automatically win more without Olympic tradition.
- Home field advantage is real but smaller than expected for dominant nations like the USA (+8 medals). It likely matters more for mid-tier nations.
- Data cleaning (country code mapping, format reshaping) took as much time as modelling — this is normal in real data science work.
- SHAP explainability is as important as model accuracy for communicating results to non-technical audiences.

---

## Potential Improvements

- Find a dataset including 2020 Tokyo and 2024 Paris results for more recent validation
- Add sport-specific predictions (athletics, swimming, gymnastics separately)
- Include population as a feature alongside GDP
- Bayesian model for uncertainty intervals on each prediction
- Geopolitical features (sanctions, boycotts) for edge case handling

---

## Author

Niko Komljenović — [LinkedIn](https://www.linkedin.com/in/niko-komljenovi%C4%87-b5bbba2a9/) · [GitHub](https://github.com/nOObY098)
