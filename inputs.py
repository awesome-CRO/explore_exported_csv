import pandas as pd
import streamlit as st


def fetch_data(hint: str) -> pd.DataFrame:
    uploaded_file = st.sidebar.file_uploader(label=hint)
    if uploaded_file is not None:
        return construct_timestamp_index(pd.read_csv(uploaded_file))
    else:
        return pd.DataFrame()


def fetch_crypto_wallet_history() -> pd.DataFrame:
    return fetch_data('Crypto Wallet Histrory (CSV)')


def fetch_fiat_wallet_history() -> pd.DataFrame:
    return fetch_data('Fiat Wallet Histrory (CSV)')


def fetch_visa_card_history() -> pd.DataFrame:
    return fetch_data('Visa Card Histrory (CSV)')


def construct_timestamp_index(data: pd.DataFrame) -> pd.DataFrame:
    data.index = pd.to_datetime(data['Timestamp (UTC)'],
                                format='%Y-%m-%d %H:%M:%S')
    return data.drop(columns=['Timestamp (UTC)'])


def fetch_feature_flags() -> set[str]:
    default_features = ['summary', 'monthly_spending', 'spending_by_category']
    optional_features = ['raw_table']
    return set(
        st.sidebar.multiselect('Features',
                               default_features + optional_features,
                               default_features))
