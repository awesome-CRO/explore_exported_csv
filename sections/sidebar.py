import pandas as pd
from globals.config import GlobalConfigSingleton
from inputs import (fetch_crypto_wallet_history, fetch_feature_flags,
                    fetch_fiat_wallet_history, fetch_visa_card_history)


def sidebar_section() -> None:
    config = GlobalConfigSingleton.get()
    config.crypto_wallet_history = fetch_crypto_wallet_history()
    config.fiat_wallet_history = fetch_fiat_wallet_history()
    config.visa_card_history = fetch_visa_card_history()
    config.features = fetch_feature_flags()

    config.combined_history = pd.concat([
        config.crypto_wallet_history, config.fiat_wallet_history,
        config.visa_card_history
    ])