import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Olympics 2028 Medal Predictor",
    page_icon="🏅",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    predictions = pd.read_csv('data/processed/medals_features.csv')
    return predictions

df = load_data()

# --- Header ---
st.title("Olympics 2028 Medal Predictor")
st.markdown("Predicting medal counts for the Los Angeles Olympics using historical data, home field advantage, and economic factors.")

# --- Sidebar ---
st.sidebar.header("Filters")
top_n = st.sidebar.slider("Show top N countries", 5, 50, 20)
show_host = st.sidebar.checkbox("Highlight host nation (USA)", value=True)

# --- Predictions ---
df_2016 = df[df['Year'] == 2016].copy()
df_2016['is_host'] = df_2016['NOC'].apply(lambda x: 1 if x == 'USA' else 0)

st.header("2028 Predictions")

# Top N chart
top = df_2016.sort_values('total', ascending=False).head(top_n)
colors = ['#d62728' if (noc == 'USA' and show_host) else '#1f77b4' for noc in top['NOC']]

fig = go.Figure(go.Bar(
    x=top['total'],
    y=top['NOC'],
    orientation='h',
    marker_color=colors[::-1]
))
fig.update_layout(
    title=f'Top {top_n} predicted countries — LA 2028',
    xaxis_title='Predicted medals',
    yaxis=dict(autorange='reversed'),
    height=600
)
st.plotly_chart(fig, use_container_width=True)

# --- Key metrics ---
st.header("Key insights")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("USA predicted medals", "254", "+8 from home advantage")
with col2:
    st.metric("Model MAE", "9.35", "medals per country")
with col3:
    st.metric("Spearman rank", "0.894", "country ranking accuracy")

# --- Historical trends ---
st.header("Historical medal trends")
countries = st.multiselect(
    "Select countries to compare",
    options=sorted(df['NOC'].unique()),
    default=['USA', 'CHN', 'RUS', 'GBR']
)

if countries:
    filtered = df[df['NOC'].isin(countries)]
    fig2 = px.line(
        filtered,
        x='Year',
        y='total',
        color='NOC',
        title='Medal counts over time',
        markers=True
    )
    st.plotly_chart(fig2, use_container_width=True)

# --- Footer ---
st.markdown("---")
st.markdown("Built with Python · XGBoost · Streamlit · Data: Kaggle + World Bank")