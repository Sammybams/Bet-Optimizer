import streamlit as st
st.set_page_config(page_title="Bet Optimizer App", page_icon="🎯")

st.title('Bet Optimizer 🎯')

import os
import numpy as np
import pandas as pd
from dotenv import load_dotenv
load_dotenv('secrets.env')

weights_url = os.environ.get("DATA")

weights = pd.read_parquet(weights_url)