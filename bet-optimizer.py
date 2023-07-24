import streamlit as st
st.set_page_config(page_title="Bet Optimizer App", page_icon="🎯")

st.title('Bet Optimizer 🎯')

from dotenv import load_dotenv
load_dotenv('secrets.env')