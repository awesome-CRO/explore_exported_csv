import streamlit as st
from globals.config import GlobalConfigSingleton


def overview_section() -> None:
    config = GlobalConfigSingleton.get()
    st.header('Overview')
    if not config.combined_history.empty:
        investment_histroy = config.combined_history.copy()
        investment_histroy = investment_histroy[
            (investment_histroy['Currency'] == 'USD')
            & (investment_histroy['Transaction Kind'] == 'van_purchase')]
        staking_reward = config.combined_history[
            config.combined_history['Transaction Kind'] ==
            'mco_stake_reward']['Amount'].sum()
        cashback = config.combined_history[
            config.combined_history['Transaction Kind'] ==
            'referral_card_cashback']['Amount'].sum()
        mission_reward = config.combined_history[
            config.combined_history['Transaction Description'] ==
            'Mission Rewards Deposit']['Amount'].sum()
        direct_purchase_table = config.combined_history[
            config.combined_history['Transaction Description'].str.contains(
                '^Buy ')]
        direct_purchase_investment = direct_purchase_table[
            'Native Amount'].sum()
        estimated_direct_purchase_fees = direct_purchase_investment * 1.25 / 100
        fiat_purchase = -investment_histroy['Amount'].sum()
        total_investment = direct_purchase_investment + fiat_purchase
        total_cro_rewards = cashback + mission_reward + staking_reward
        if 'summary' in config.features:
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
        if 'raw_table' in config.features:
            st.subheader('Combined Table')
            st.write(config.combined_history)
            st.subheader('Initial Investment Table')
            st.write(investment_histroy)
            st.subheader('Direct Purchase Table')
            st.write(direct_purchase_table)