from typing import List
import pandas as pd
import streamlit as st


def fetch_data(hint: str) -> pd.DataFrame:
    uploaded_file = st.sidebar.file_uploader(label=hint)
    return pd.read_csv(
        uploaded_file) if uploaded_file is not None else pd.DataFrame()


def fetch_crypto_wallet_history() -> pd.DataFrame:
    return fetch_data('Crypto Wallet Histrory (CSV)')


def fetch_fiat_wallet_history() -> pd.DataFrame:
    return fetch_data('Fiat Wallet Histrory (CSV)')


def fetch_visa_card_history() -> pd.DataFrame:
    return fetch_data('Visa Card Histrory (CSV)')


def fetch_native_currency() -> List[str]:
    selected_native_currency = st.sidebar.multiselect(
        'What is your native currency?', ['USD', 'CAD'], ['USD'])
    return selected_native_currency