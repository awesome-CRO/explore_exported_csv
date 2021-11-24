from globals.config import GlobalConfigSingleton
import streamlit as st

from stats.coin_specific import CoinAnalyzer


def crypto_wallet_section() -> None:
    config = GlobalConfigSingleton.get()
    st.header('Crypto Wallet')
    if not config.crypto_wallet_history.empty:
        cro_analyzer = CoinAnalyzer(config.combined_history, 'CRO')
        if 'raw_table' in config.features:
            st.subheader('CRO Related Transactions')
            st.write(cro_analyzer.related)
        if 'summary' in config.features:
            avg_cost, amount, cost = cro_analyzer.get_crypto_purchase_summary()
            row = st.columns(3)
            row[0].metric("Average Cost",
                          '$ {0} / CRO'.format(round(avg_cost, 2)))
            row[1].metric("Total Amount", '{0} CRO'.format(amount))
            row[2].metric("Total Cost", '$ {0}'.format(cost))
    else:
        st.warning('Crypto wallet history has not been uploaded')