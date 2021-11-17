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
    staking_reward = combined_history[combined_history['Transaction Kind'] ==
                                      'mco_stake_reward']['Amount'].sum()
    cashback = combined_history[combined_history['Transaction Kind'] ==
                                'referral_card_cashback']['Amount'].sum()
    mission_reward = combined_history[
        combined_history['Transaction Description'] ==
        'Mission Rewards Deposit']['Amount'].sum()
    direct_purchase_table = combined_history[
        combined_history['Transaction Description'].str.contains('^Buy ')]
    direct_purchase_investment = direct_purchase_table['Native Amount'].sum()
    estimated_direct_purchase_fees = direct_purchase_investment * 1.25 / 100
    fiat_purchase = -investment_histroy['Amount'].sum()
    total_investment = direct_purchase_investment + fiat_purchase
    total_cro_rewards = cashback + mission_reward + staking_reward
    if 'summary' in features:
        st.subheader('Summary')
        r1 = st.columns(3)
        r1[0].metric(label='Total Investment',
                     value='$ {0}'.format(int(total_investment)))
        r1[1].metric(label='Direct Purchase Amount (Fee)',
                     delta='-${0} Fee (estimated at 1.25%)'.format(
                         int(estimated_direct_purchase_fees)),
                     value='$ {0}'.format(int(direct_purchase_investment)))
        r1[2].metric(label='Fiat Purchase Amount',
                     value='$ {0}'.format(int(fiat_purchase)))
        st.info('''
                Fiat purchase: crypto purchase made from the
                fiat wallet which in general do not incur fees.\n
                Direct purchase: crypto purchase made from credit
                or debit card which has a fee of roughly 1.25%.
                ''')
        st.warning('''
                   For now, the summary does not take withdraw into
                   consideration. For example, if you invested $1000
                   and then withdraw $200, the total investment shown
                   will be $1000 instead of $800. This is the current
                   limitation (since I have not yet taken any profit)
                   and can be added in the future should there be a need.
                   ''')
        st.metric(label='Total CRO Reward (excluding earn)',
                  value='{0} CRO'.format(int(total_cro_rewards)))
        reward_row = st.columns(3)
        reward_row[0].metric(label='CRO Staking Reward',
                             value='{0} CRO'.format(int(staking_reward)))
        reward_row[1].metric(label='Cashback Reward',
                             value='{0} CRO'.format(int(cashback)))
        reward_row[2].metric(label='Total Mission Reward',
                             value='{0} CRO'.format(int(mission_reward)))
    if 'raw_table' in features:
        st.subheader('Combined Table')
        st.write(combined_history)
        st.subheader('Initial Investment Table')
        st.write(investment_histroy)
        st.subheader('Direct Purchase Table')
        st.write(direct_purchase_table)

st.header('Visa Card')
if not visa_card_history.empty:
    if 'raw_table' in features:
        st.subheader('Visa Card Transaction Table')
        st.write(visa_card_history)
    if 'spending_by_category' in features:
        spending_by_categories_table = visa_card_history.copy()
        spending_by_categories_table = spending_by_categories_table[
            spending_by_categories_table['Amount'] < 0]
        spending_by_categories_table[
            'Amount'] = spending_by_categories_table['Amount'] * -1
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
