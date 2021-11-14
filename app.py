import streamlit as st
import pandas as pd
from inputs import (fetch_crypto_wallet_history, fetch_feature_flags,
                    fetch_fiat_wallet_history, fetch_visa_card_history)

st.set_page_config(initial_sidebar_state='expanded')

st.title('Crypto.com History Analysis')

crypto_wallet_history = fetch_crypto_wallet_history()
fiat_wallet_history = fetch_fiat_wallet_history()
visa_card_history = fetch_visa_card_history()
features = fetch_feature_flags()

combined_history = pd.concat(
    [crypto_wallet_history, fiat_wallet_history, visa_card_history])

st.header('Overview')
if not combined_history.empty:
    investment_histroy = combined_history.copy()
    investment_histroy = investment_histroy[
        (investment_histroy['Currency'] == 'USD')
        & (investment_histroy['Transaction Kind'] == 'van_purchase')]
    if 'summary' in features:
        st.subheader('Summary')
        col1, col2, col3 = st.columns(3)
        total_investment = -investment_histroy['Amount'].sum()
        col1.metric(label='Total Investment',
                    value='$ {0}'.format(int(total_investment)))
        staking_reward = combined_history[combined_history['Transaction Kind']
                                          ==
                                          'mco_stake_reward']['Amount'].sum()
        col2.metric(label='CRO Staking Reward',
                    value='{0} CRO'.format(int(staking_reward)))
        cashback = combined_history[combined_history['Transaction Kind'] ==
                                    'referral_card_cashback']['Amount'].sum()
        col3.metric(label='Cashback Reward',
                    value='{0} CRO'.format(int(cashback)))
    if 'raw_table' in features:
        st.subheader('Combined Table')
        st.write(combined_history)
        st.subheader('Initial Investment Table')
        st.write(investment_histroy)

st.header('Visa Card')
if not visa_card_history.empty:
    if 'raw_table' in features:
        st.subheader('Visa Card Transaction Table')
        st.write(visa_card_history)
    if 'spending_by_category' in features:
        spending_by_categories_table = visa_card_history.copy()
        spending_by_categories_table = spending_by_categories_table[spending_by_categories_table['Amount'] < 0]
        spending_by_categories_table['Amount'] = spending_by_categories_table['Amount'] * -1
        spending_by_categories_table = spending_by_categories_table[[
            'Transaction Description', 'Amount'
        ]].groupby(['Transaction Description']).sum()
        st.subheader('Spending by Category')
        st.bar_chart(spending_by_categories_table)
    if 'monthly_spending' in features:
        spending = visa_card_history.copy()
        spending = spending[spending['Native Amount'] < 0][['Native Amount'
                                                            ]].copy()
        spending['Native Amount'] = spending['Native Amount'].apply(
            lambda x: -x)
        monthly_spending = spending.groupby(pd.Grouper(freq='M')).sum()
        st.subheader('Monthly spending')
        st.bar_chart(monthly_spending)
else:
    st.warning('Visa card history has not been uploaded')

st.header('Crypto Wallet')
if not crypto_wallet_history.empty:
    pass
else:
    st.warning('Crypto wallet history has not been uploaded')

st.header('Fiat Wallet')
if not fiat_wallet_history.empty:
    pass
else:
    st.warning('Fiat wallet history has not been uploaded')