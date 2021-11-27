from globals.config import GlobalConfigSingleton
from stats.coin_specific import CoinAnalyzer
import streamlit as st


def van_purchase_section(analyzer: CoinAnalyzer) -> None:
    config = GlobalConfigSingleton.get()
    if 'summary' in config.features:
        st.subheader('CRO Van Purchase Summary')
        summary = analyzer.van_purchase_summary
        c1, c2, c3 = st.columns(3)
        c1.metric("Average Cost",
                  '$ {0} / CRO'.format(round(summary['avg'], 2)))
        c2.metric("Total Amount", '{0} CRO'.format(round(summary['amount'],
                                                         2)))
        c3.metric("Total Cost", '$ {0}'.format(round(summary['cost'], 2)))
    if 'raw_table' in config.features:
        st.subheader('Van Purchase Transactions')
        st.write(analyzer.van_purchases)