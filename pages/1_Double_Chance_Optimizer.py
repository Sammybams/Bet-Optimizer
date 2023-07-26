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
odds_a = st.number_input('Enter odds for Single chance (Win | Lose | Draw)', min_value=1.01)
odds_b = st.number_input('Enter odds for Double chance (Win or Draw | Lose or Draw | Win or Lose)', min_value=1.01)

def opt_details(stake_single, stake_double, reward_single, reward_double, odds_a=odds_a, odds_b=odds_b):
    output = f"""
            | Scenario | Odds | Stake | Reward |
            |------------------|------------------|------------------|------------------|
            | Single | {odds_a} | {stake_single} | {reward_single} |
            | Double-chance | {odds_b} | {stake_double} | {reward_double} |
            """
    return output


if st.button("Optimize"):

    score = []
    try:
        for i, value in enumerate(weights):
            w_a, w_b = value
            a_wa = odds_a*w_a
            b_wb = odds_b*w_b
            
            score.append([i, [a_wa, b_wb]])

        sorted_scores = sorted(score, key = lambda x: min(x[1]))
        weights_best_score = weights[sorted_scores[-1][0]]
        best_score = sorted_scores[-1][1]

        stake_single = round(amount*weights_best_score[0],3)
        stake_double = round(amount*weights_best_score[1],3)

        reward_single = round(amount*best_score[0],3)
        reward_double = round(amount*best_score[1],3)

        best_payout = max([reward_single, reward_double])
        min_payout = min([reward_single, reward_double])

        if min(best_score) < 1:
            st.warning(f'Not optimizable for zero loss.', icon="⚠️")
            cases = []
            weights_cases = []
            size = len(sorted_scores)

            for i in range(1,size):
                if max(sorted_scores[-i][1])>1.05:
                    cases.append(sorted_scores[-i][1])
                    weights_cases.append(weights[sorted_scores[-i][0]])
                    break

            for i in range(1,size):
                if max(sorted_scores[-i][1])>1.1:
                    cases.append(sorted_scores[-i][1])
                    weights_cases.append(weights[sorted_scores[-i][0]])
                    break

            for i in range(1,size):
                if max(sorted_scores[-i][1])>1.2:
                    cases.append(sorted_scores[-i][1])
                    weights_cases.append(weights[sorted_scores[-i][0]])
                    break

            for i in range(1,size):
                if max(sorted_scores[-i][1])>1.3:
                    cases.append(sorted_scores[-i][1])
                    weights_cases.append(weights[sorted_scores[-i][0]])
                    break

            for i in range(1,size):
                if max(sorted_scores[-i][1])>1.4:
                    cases.append(sorted_scores[-i][1])
                    weights_cases.append(weights[sorted_scores[-i][0]])
                    break
                
            for i in range(1,size):
                if max(sorted_scores[-i][1])>1.5:
                    cases.append(sorted_scores[-i][1])
                    weights_cases.append(weights[sorted_scores[-i][0]])
                    break

            st.subheader("Alternative Strategies to Diversify Portfolio")
            
            case1 = [round(((1-min(cases[0]))*100), 2), round(((max(cases[0])-1)*100), 2)]
            case2 = [round(((1-min(cases[1]))*100), 2), round(((max(cases[1])-1)*100), 2)]
            case3 = [round(((1-min(cases[2]))*100), 2), round(((max(cases[2])-1)*100), 2)]
            case4 = [round(((1-min(cases[3]))*100), 2), round(((max(cases[3])-1)*100), 2)]
            case5 = [round(((1-min(cases[4]))*100), 2), round(((max(cases[4])-1)*100), 2)]
            case6 = [round(((1-min(cases[5]))*100), 2), round(((max(cases[5])-1)*100), 2)]
            
            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([f"{case1[0]}% Loss | {case1[1]}% Profit", f"{case2[0]}% Loss | {case2[1]}% Profit",
                                                        f"{case3[0]}% Loss | {case3[1]}% Profit", f"{case4[0]}% Loss | {case4[1]}% Profit",
                                                        f"{case5[0]}% Loss | {case5[1]}% Profit", f"{case6[0]}% Loss | {case6[1]}% Profit"])

            no_opt_stake_single = []
            no_opt_stake_double = []

            no_opt_reward_single = []
            no_opt_reward_double = []
            for i in range(6):
                no_opt_stake_single.append(round(amount*weights_cases[i][0],3))
                no_opt_stake_double.append(round(amount*weights_cases[i][1],3))

                no_opt_reward_single.append(round(amount*cases[i][0],3))
                no_opt_reward_double.append(round(amount*cases[i][1],3))

            # 5% profit
            tab1.markdown(opt_details(no_opt_stake_single[0], no_opt_stake_double[0],
                                      no_opt_reward_single[0], no_opt_reward_double[0]))
            tab1.markdown("")
            tab1.markdown(f'##### Best possible payout is {max([no_opt_stake_single[0], no_opt_stake_double[0]])}.')
            tab1.markdown(f'##### Worst possible payout is {min([no_opt_reward_single[0], no_opt_reward_double[0]])}.')

            # 10% profit
            tab2.markdown(opt_details(no_opt_stake_single[1], no_opt_stake_double[1],
                                      no_opt_reward_single[1], no_opt_reward_double[1],))
            tab2.markdown("")
            tab2.markdown(f'##### Best possible payout is {max([no_opt_stake_single[1], no_opt_stake_double[1]])}.')
            tab2.markdown(f'##### Worst possible payout is {min([no_opt_reward_single[1], no_opt_reward_double[1]])}.')
            
            # 20% profit
            tab3.markdown(opt_details(no_opt_stake_single[2], no_opt_stake_double[2],
                                      no_opt_reward_single[2], no_opt_reward_double[2],))
            tab3.markdown("")
            tab3.markdown(f'##### Best possible payout is {max([no_opt_stake_single[2], no_opt_stake_double[2],])}.')
            tab3.markdown(f'##### Worst possible payout is {min([no_opt_reward_single[2], no_opt_reward_double[2]])}.')

            # 30% profit
            tab4.markdown(opt_details(no_opt_stake_single[3], no_opt_stake_double[3],
                                      no_opt_reward_single[3], no_opt_reward_double[3],))
            tab4.markdown("")
            tab4.markdown(f'##### Best possible payout is {max([no_opt_stake_single[3], no_opt_stake_double[3]])}.')
            tab4.markdown(f'##### Worst possible payout is {min([no_opt_reward_single[3], no_opt_reward_double[3]])}.')
            
            # 40% profit
            tab5.markdown(opt_details(no_opt_stake_single[4], no_opt_stake_double[4],
                                      no_opt_reward_single[4], no_opt_reward_double[4]))
            tab5.markdown("")
            tab5.markdown(f'##### Best possible payout is {max([no_opt_stake_single[4], no_opt_stake_double[4]])}.')
            tab5.markdown(f'##### Worst possible payout is {min([no_opt_reward_single[4], no_opt_reward_double[4]])}.')

            # 50% profit
            tab6.markdown(opt_details(no_opt_stake_single[5], no_opt_stake_double[5],
                                      no_opt_reward_single[5], no_opt_reward_double[5]))
            tab6.markdown("")
            tab6.markdown(f'##### Best possible payout is {max([no_opt_stake_single[5], no_opt_stake_double[5]])}.')
            tab6.markdown(f'##### Worst possible payout is {min([no_opt_reward_single[5], no_opt_reward_double[5]])}.')

        else:
            st.success(f'Betting portfolio optimized. Best possible payout is {best_payout}.', icon="✅")
            st.markdown(opt_details(stake_single, stake_double, reward_single, reward_double))
            st.markdown("")
            st.markdown(f'##### Guranteed minimum payout is {min_payout}.')

        # coming soon charts.
        # grouping = np.array(sorted_scores)[:,1].T
        # plot_data = pd.DataFrame(columns=['Win', 'Draw', 'Lose'])
        # plot_data['Win'] = grouping[0]
        # plot_data['Draw'] = grouping[1]
        # plot_data['Lose'] = grouping[2]

        # st.line_chart(plot_data, x=plot_data.index, y='Normalized Payout')
    except:
        st.warning(f'Invalid inputs.', icon="⚠️")
