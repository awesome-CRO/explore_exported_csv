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
        self.crypto_purchase_summary = self._get_crypto_purchase_summary()
        self.van_purchase_summary = self._get_van_purchase_summary()
        self.exchange_purchase_summary = self._get_exchange_purchase_summary()
        # The overall summary should be calculated at the end
        self.overall_summary = self._get_overall_summary()

    def _get_overall_summary(self) -> Tuple[float, float, float]:
        overall_amount = sum([
            self.crypto_purchase_summary['amount'],
            self.van_purchase_summary['amount'],
            self.exchange_purchase_summary['amount']
        ])
        overall_cost = sum([
            self.crypto_purchase_summary['cost'],
            self.van_purchase_summary['cost'],
            self.exchange_purchase_summary['cost']
        ])
        avg_cost = overall_cost / overall_amount
        return {
            'avg': avg_cost,
            'amount': overall_amount,
            'cost': overall_cost
        }

    def _get_crypto_purchase_summary(self) -> Tuple[float, float, float]:
        amount = self.crypto_purchases['Amount'].sum()
        cost = self.crypto_purchases['Native Amount'].sum()
        avg_cost = cost / amount
        return {'avg': avg_cost, 'amount': amount, 'cost': cost}

    def _get_van_purchase_summary(self) -> Tuple[float, float, float]:
        amount = self.van_purchases['To Amount'].sum()
        cost = self.van_purchases['Native Amount'].sum()
        avg_cost = cost / amount
        return {'avg': avg_cost, 'amount': amount, 'cost': cost}

    def _get_exchange_purchase_summary(self) -> Tuple[float, float, float]:
        amount = self.buy_crypto_exchanges['To Amount'].sum()
        cost = self.buy_crypto_exchanges['Native Amount'].sum()
        avg_cost = cost / amount
        return {'avg': avg_cost, 'amount': amount, 'cost': cost}
