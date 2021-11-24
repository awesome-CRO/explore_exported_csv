import streamlit as st
from globals.config import GlobalConfigSingleton


def fiat_wallet_section() -> None:
    config = GlobalConfigSingleton.get()
    st.header('Fiat Wallet')
    if not config.fiat_wallet_history.empty:
        st.warning('This section is still WIP')
    else:
        st.warning('Fiat wallet history has not been uploaded')