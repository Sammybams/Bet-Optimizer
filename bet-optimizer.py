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
    # weights_url = os.environ.get("DATA")
    weights_url = st.secrets.bet_weights.URL
    weights = pd.read_parquet(weights_url).values
    return weights

# from st_files_connection import FilesConnection
# conn = st.experimental_connection('bet_weights', type=FilesConnection)
# weights = conn.read(st.secrets.bet_weights.url, input_format='parquet').values

weights = load_data()

amount = st.number_input('Enter total amount for bet', min_value=0.01)
odds_a = st.number_input('Enter odds for win', min_value=1.01)
odds_b = st.number_input('Enter odds for draw', min_value=1.01)
odds_c = st.number_input('Enter odds for lose', min_value=1.01)

def opt_details(stake_win, stake_draw, stake_lose, reward_win, reward_draw, reward_lose, odds_a=odds_a, odds_b=odds_b, odds_c=odds_c):
    output = f"""
            | Scenario | Odds | Stake | Reward |
            |------------------|------------------|------------------|------------------|
            | Win 🏅 | {odds_a} |{stake_win} | {reward_win} |
            | Draw 🤝 | {odds_b} | {stake_draw} | {reward_draw} |
            | Lose 👎 | {odds_c} | {stake_lose} | {reward_lose} |
            """
    return output

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
            |------------------|------------------|------------------|------------------|
            | Win 🏅 | {odds_a} |{stake_win} | {reward_win} |
            | Draw 🤝 | {odds_b} | {stake_draw} | {reward_draw} |
            | Lose 👎 | {odds_c} | {stake_lose} | {reward_lose} |
            """
    best_payout = max([reward_win, reward_draw, reward_lose])
    min_payout = min([reward_win, reward_draw, reward_lose])

    if min(best_score) < 1:
        st.warning(f'Not optimizable for zero loss. Best possible payout to avoid total loss is {best_payout}.', icon="⚠️")
        cases = []
        st.subheader("Alternative Strategies to Diversify Portfolio")
        case1 = [(1 - round(min(cases[0]), 2))*100, (round(max(cases[0]), 2) - 1)*100]
        case2 = [(1 - round(min(cases[1]), 2))*100, (round(max(cases[1]), 2) - 1)*100]
        case3 = [(1 - round(min(cases[2]), 2))*100, (round(max(cases[2]), 2) - 1)*100]
        case4 = [(1 - round(min(cases[3]), 2))*100, (round(max(cases[3]), 2) - 1)*100]
        case5 = [(1 - round(min(cases[4]), 2))*100, (round(max(cases[4]), 2) - 1)*100]
        case6 = [(1 - round(min(cases[5]), 2))*100, (round(max(cases[5]), 2) - 1)*100]

        
        tab1, tab2, tab3, tab4, tab5 = st.tabs([f"{case1[0]}% Loss | {case1[1]}% Profit", f"{case2[0]}% Loss | {case2[1]}% Profit", f"{case3[0]}% Loss | {case3[1]}% Profit", 
                                                f"{case4[0]}% Loss | {case4[1]}% Profit", f"{case5[0]}% Loss | {case5[1]}% Profit", f"{case6[0]}% Loss | {case6[1]}% Profit"])
        st.markdown(opt_details(stake_win, stake_draw, stake_lose, reward_win, reward_draw, reward_lose))

    else:
        st.success(f'Betting portfolio optimized. Best possible payout is {best_payout}.', icon="✅")
        st.markdown(opt_details(stake_win, stake_draw, stake_lose, reward_win, reward_draw, reward_lose))
        st.markdown(f'#### Guranteed minimum payout is {min_payout}.')

st.divider()
st.markdown("Built by [Samuel Bamgbola](https://www.linkedin.com/in/samuel-bamgbola-29baa91a3/).", unsafe_allow_html=True)