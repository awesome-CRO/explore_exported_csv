import streamlit as st
import pandas as pd
from globals.config import GlobalConfigSingleton


def visa_card_section() -> None:
    config = GlobalConfigSingleton.get()
    st.header('Visa Card')
    if not config.visa_card_history.empty:
        st.warning('This section is still WIP')
        if 'raw_table' in config.features:
            st.subheader('Visa Card Transaction Table')
            st.write(config.visa_card_history)
        if 'spending_by_category' in config.features:
            spending_by_categories_table = config.visa_card_history.copy()
            spending_by_categories_table = spending_by_categories_table[
                spending_by_categories_table['Amount'] < 0]
            spending_by_categories_table[
                'Amount'] = spending_by_categories_table['Amount'] * -1
            spending_by_categories_table = spending_by_categories_table[[
                'Transaction Description', 'Amount'
            ]].groupby(['Transaction Description']).sum()
            st.subheader('Spending by Category')
            st.bar_chart(spending_by_categories_table)
        if 'monthly_spending' in config.features:
            spending = config.visa_card_history.copy()
            spending = spending[spending['Native Amount'] < 0][[
                'Native Amount'
            ]].copy()
            spending['Native Amount'] = spending['Native Amount'].apply(
                lambda x: -x)
            monthly_spending = spending.groupby(pd.Grouper(freq='M')).sum()
            st.subheader('Monthly spending')
            st.bar_chart(monthly_spending)
    else:
        st.warning('Visa card history has not been uploaded')