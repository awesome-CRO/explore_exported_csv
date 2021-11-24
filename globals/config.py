import pandas as pd


class GlobalConfig:
    def __init__(self) -> None:
        self.crypto_wallet_history = pd.DataFrame()
        self.fiat_wallet_history = pd.DataFrame()
        self.visa_card_history = pd.DataFrame()
        self.features = set()


class GlobalConfigSingleton:
    _instance = None

    @classmethod
    def get(cls) -> GlobalConfig:
        if cls._instance is None:
            cls._instance = GlobalConfig()
        return cls._instance