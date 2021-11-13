import streamlit as st
import pandas as pd
from inputs import (fetch_crypto_wallet_history, fetch_fiat_wallet_history,
                    fetch_visa_card_history, fetch_native_currency)

st.title('Crypto.com History Analysis')

st.sidebar.title('Settings')
crypto_wallet_history = fetch_crypto_wallet_history()
fiat_wallet_history = fetch_fiat_wallet_history()
visa_card_history = fetch_visa_card_history()
native_currency = fetch_native_currency()

combined_history = pd.concat([crypto_wallet_history, fiat_wallet_history, visa_card_history])

if not combined_history.empty:
    st.write(combined_history)
