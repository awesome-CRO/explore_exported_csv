from globals.config import GlobalConfigSingleton
import streamlit as st
from sections.crypto_wallet.crypto_purchase import crypto_purchase_section

from stats.coin_specific import CoinAnalyzer


def crypto_wallet_section() -> None:
    config = GlobalConfigSingleton.get()
    st.header('Crypto Wallet')
    if not config.crypto_wallet_history.empty:
        cro_analyzer = CoinAnalyzer(config.combined_history, 'CRO')
        crypto_purchase_section(cro_analyzer)
        if 'summary' in config.features:
            # This row is for van CRO purchases
            st.subheader('CRO Van Purchase Summary')
            avg_cost, amount, cost = cro_analyzer.get_van_purchase_summary()
            row_van_buy = st.columns(3)
            row_van_buy[0].metric("Average Cost",
                                  '$ {0} / CRO'.format(round(avg_cost, 2)))
            row_van_buy[1].metric("Total Amount", '{0} CRO'.format(amount))
            row_van_buy[2].metric("Total Cost", '$ {0}'.format(cost))
            # This row is for incoming CRO exchanges
            st.subheader('CRO Purchase from Coin Exchange')
            avg_cost, amount, cost = cro_analyzer.get_crypto_purchase_exchange_summary(
            )
            row_exchange_buy = st.columns(3)
            row_exchange_buy[0].metric(
                "Average Cost", '$ {0} / CRO'.format(round(avg_cost, 2)))
            row_exchange_buy[1].metric("Total Amount",
                                       '{0} CRO'.format(amount))
            row_exchange_buy[2].metric("Total Cost", '$ {0}'.format(cost))
        if 'raw_table' in config.features:
            st.subheader('CRO Related Transactions')
            st.write(cro_analyzer.related)
            st.subheader('Van Purchase Transactions')
            st.write(cro_analyzer.van_purchases)
            st.subheader('Crypto Purchase Exchange Transactions')
            st.write(cro_analyzer.buy_crypto_exchanges)
    else:
        st.warning('Crypto wallet history has not been uploaded')