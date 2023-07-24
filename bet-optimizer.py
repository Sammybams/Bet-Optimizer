import streamlit as st
st.set_page_config(page_title="Bet Optimizer App", page_icon="🎯")

st.title('Bet Optimizer 🎯')

import os
import numpy as np
import pandas as pd
from dotenv import load_dotenv
load_dotenv('secrets.env')

weights_url = os.environ.get("DATA")

weights = pd.read_parquet(weights_url).values

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
    best_score = sorted_scores[-1][1]
    loc_best_score = weights[sorted_scores[-1][0]]

    if best_score <= 1:
        st.warning('Not optimizable for lose', icon="⚠️")

        stake_win = amount*best_score[0]
        stake_draw = amount*best_score[1]
        stake_lose = amount*best_score[2]

        output = f"""
                | Scenario | Stake |
                |------------------|------------------|
                | Win | {stake_win} |
                | Draw | {stake_draw} |
                | Lose | {stake_lose} |
                """


