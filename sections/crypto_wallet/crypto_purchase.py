from globals.config import GlobalConfigSingleton
from stats.coin_specific import CoinAnalyzer
import streamlit as st


def crypto_purchase_section(analyzer: CoinAnalyzer) -> None:
    config = GlobalConfigSingleton.get()
    if 'summary' in config.features:
        st.subheader('CRO Direct Purchase Summary')
        avg_cost, amount, cost = analyzer.get_crypto_purchase_summary()
        row_direct_buy = st.columns(3)
        row_direct_buy[0].metric("Average Cost",
                                 '$ {0} / CRO'.format(round(avg_cost, 2)))
        row_direct_buy[1].metric("Total Amount", '{0} CRO'.format(amount))
        row_direct_buy[2].metric("Total Cost", '$ {0}'.format(cost))
    if 'raw_table' in config.features:
        st.subheader('Crypto Purchase Transactions')
        st.write(analyzer.crypto_purchases)