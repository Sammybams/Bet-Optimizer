import streamlit as st
st.set_page_config(page_title="Bet Optimizer App", page_icon="🎯")

st.title('Bet Optimizer 🎯')

import os
import numpy as np
import pandas as pd
from dotenv import load_dotenv
load_dotenv('secrets.env')

@st.cache_data
def load_data():
    weights_url = os.environ.get("DATA")
    weights = pd.read_parquet(weights_url).values
    return weights

weights = load_data()

amount = st.number_input('Enter total amount for bet', min_value=0.01)
odds_a = st.number_input('Enter odds for win', min_value=1.01)
odds_b = st.number_input('Enter odds for draw', min_value=1.01)
odds_c = st.number_input('Enter odds for lose', min_value=1.01)

if st.button("Optimize"):

    score = []

    for i, value in enumerate(weights):
        w_a, w_b, w_c = value
        a_wa = odds_a*w_a
        b_wb = odds_b*w_b
        c_wc = odds_c*w_c
        
        score.append([i, [a_wa, b_wb, c_wc]])

    sorted_scores = sorted(score, key = lambda x: min(x[1]))
    weights_best_score = weights[sorted_scores[-1][0]]
    best_score = sorted_scores[-1][1]

    stake_win = round(amount*weights_best_score[0],3)
    stake_draw = round(amount*weights_best_score[1],3)
    stake_lose = round(amount*weights_best_score[2],3)

    reward_win = round(amount*best_score[0],3)
    reward_draw = round(amount*best_score[1],3)
    reward_lose = round(amount*best_score[2],3)

    output = f"""
            | Scenario | Odds | Stake | Reward |
            |------------------|------------------|------------------|------------------ |
            | Win | {odds_a} |{stake_win} | {reward_win} |
            | Draw | {odds_b} | {stake_draw} | {reward_draw} |
            | Lose | {odds_c} | {stake_lose} | {reward_lose} |
            """
    best_payout = max([reward_win, reward_draw, reward_lose])

    if min(best_score) < 1:
        st.warning(f'Not optimizable for zero loss. Best possible payout to avoid total loss is {best_payout}.', icon="⚠️")
        st.markdown(output)

    else:
        st.success(f'Betting portfolio optimized. Best payout is {best_payout}.', icon="✅")
        st.markdown(output)
