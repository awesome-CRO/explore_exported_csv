from globals.config import GlobalConfigSingleton
import streamlit as st
from sections.crypto_wallet.crypto_purchase import crypto_purchase_section
from sections.crypto_wallet.exchange_purchase import exchange_purchase
from sections.crypto_wallet.overall import overall_section
from sections.crypto_wallet.van_purchase import van_purchase_section

from stats.coin_specific import CoinAnalyzer


def crypto_wallet_section() -> None:
    config = GlobalConfigSingleton.get()
    st.header('Crypto Wallet')
    if not config.crypto_wallet_history.empty:
        cro_analyzer = CoinAnalyzer(config.crypto_wallet_history, 'CRO')
        overall_section(cro_analyzer)
        crypto_purchase_section(cro_analyzer)
        van_purchase_section(cro_analyzer)
        exchange_purchase(cro_analyzer)
        if 'raw_table' in config.features:
            st.subheader('CRO Related Transactions')
            st.write(cro_analyzer.related)
    else:
        st.warning('Crypto wallet history has not been uploaded')