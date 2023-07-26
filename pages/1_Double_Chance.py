import streamlit as st
st.set_page_config(page_title="Double-chance Bet Optimizer", page_icon="⚖️")

st.markdown("# Double-chance Bet Optimizer")
st.sidebar.header("Double-chance Bet Optimizer")

import pandas as pd

@st.cache_data
def load_double_chance_weights():
    # weights_url = os.environ.get("DATA")
    weights_url = st.secrets.bet_weights.DOUBLE_CHANCE_WEIGHTS_URL
    weights = pd.read_parquet(weights_url).values
    return weights

weights = load_double_chance_weights()

amount = st.number_input('Enter total amount for bet', min_value=0.01)
odds_a = st.number_input('Enter odds for Single chance (Win|Lose|Draw)', min_value=1.01)
odds_b = st.number_input('Enter odds for Double chance (Win or Draw | Lose or Draw | Win or Lose)', min_value=1.01)