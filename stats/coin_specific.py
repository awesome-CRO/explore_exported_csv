from typing import Tuple
import pandas as pd


class CoinAnalyzer:
    def __init__(self, transactions: pd.DataFrame, coin: str) -> None:
        self.coin = coin
        self.transactions = transactions
        self.related = transactions[(transactions['To Currency'] == coin)
                                    | (transactions['Currency'] == coin)]
        self.crypto_purchases = self.related[self.related['Transaction Kind']
                                             == 'crypto_purchase']
        self.van_purchases = self.related[self.related['Transaction Kind'] ==
                                          'van_purchase']
        self.sell_crypto_exchanges = self.related[
            (self.related['Transaction Kind'] == 'crypto_exchange')
            & (self.related['Currency'] == coin)]
        self.buy_crypto_exchanges = self.related[
            (self.related['Transaction Kind'] == 'crypto_exchange')
            & (self.related['To Currency'] == coin)]
        self.dust_conversions = self.related[self.related['Transaction Kind']
                                             == 'dust_conversion_credited']
        self.earn_interests = self.related[self.related['Transaction Kind'] ==
                                           'crypto_earn_interest_paid']
        self.cashback = self.related[self.related['Transaction Kind'] ==
                                     'referral_card_cashback']
        self.staking_reward = self.related[self.related['Transaction Kind'] ==
                                           'mco_stake_reward']
        self.reimbursement = self.related[self.related['Transaction Kind'] ==
                                          'reimbursement']

    def get_crypto_purchase_summary(self) -> Tuple[float, float, float]:
        amount = self.crypto_purchases['Amount'].sum()
        cost = self.crypto_purchases['Native Amount'].sum()
        avg_cost = cost / amount
        return avg_cost, amount, cost

    def get_van_purchase_summary(self) -> Tuple[float, float, float]:
        amount = self.van_purchases['To Amount'].sum()
        cost = self.van_purchases['Native Amount'].sum()
        avg_cost = cost / amount
        return avg_cost, amount, cost

    def get_crypto_purchase_exchange_summary(
            self) -> Tuple[float, float, float]:
        amount = self.buy_crypto_exchanges['To Amount'].sum()
        cost = self.buy_crypto_exchanges['Native Amount'].sum()
        avg_cost = cost / amount
        return avg_cost, amount, cost
