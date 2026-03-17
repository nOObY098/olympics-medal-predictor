# Olympics 2028 Medal Predictor

Predicting gold, silver, and bronze medal counts for the 2028 Los Angeles Olympics using historical data, with a focus on **home field advantage** and **economic factors**.

---

## Results

| Metric | Score |
|--------|-------|
| MAE (medals per country) | _fill after training_ |
| Spearman rank correlation | _fill after training_ |
| Backtest (Tokyo 2020) | _fill after validation_ |

> Key finding: _Summarize your most interesting result here — e.g. "Home field advantage adds an estimated X medals on average for the host nation."_

---

## Live Demo

[Streamlit Dashboard →](https://your-app-link.streamlit.app) _(deploy in Phase 5)_

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
- **Medal history**: [Kaggle — 120 Years of Olympic History](https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results)
- **Economic data**: World Bank GDP & GDP per capita (1960–2024)
- **Host nation history**: manually compiled from Wikipedia

### Key Features Engineered
- `is_host` — binary flag for the host nation
- `home_boost_multiplier` — historical medal lift for past host nations
- `rolling_3game_avg` — rolling medal average across last 3 Olympics
- `gdp_per_capita` — economic proxy for sport investment capacity
- `gdp_sport_index` — composite of GDP + estimated sport spending

### Model
- **Baseline**: Poisson regression (natural fit for count data)
- **Final model**: XGBoost regressor, tuned via time-series cross-validation
- **Validation**: Train on 1984–2016, test on Tokyo 2020, predict 2028 LA

---

## How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the full analysis
jupyter notebook notebooks/olympics_predictor.ipynb

# 3. Launch the dashboard
streamlit run app/streamlit_app.py
```

---

## Challenges & Decisions

_Fill this in as you go — employers read this section carefully._

- **Country name standardisation**: Kaggle uses "USA", World Bank uses "United States". Resolved by building a country name mapping dictionary in `src/features.py`.
- _Add more as you encounter them..._

---

## What I Learned

_Write 3–5 honest sentences at the end of the project. What surprised you? What would you do differently?_

---

## Author

Your Name — [LinkedIn](https://linkedin.com) · [GitHub](https://github.com)
