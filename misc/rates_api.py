from pycoingecko import CoinGeckoAPI
from datetime import datetime

class RatesApi:
    def __init__(self):
        self.cg = CoinGeckoAPI()

    def ping(self):
        return self.cg.ping()

    def get_supported_vs_currencies(self):
        return self.cg.get_supported_vs_currencies()

    def get_coins_list(self):
        return self.cg.get_coins_list()

    def get_asset_platforms(self):
        return self.cg.get_asset_platforms()

    def get_coins_categories_list(self):
        return self.cg.get_coins_categories_list()

    def get_coins_categories(self):
        return self.cg.get_coins_categories()

    def get_exchanges_list(self):
        return self.cg.get_exchanges_list()

    def get_exchanges_id_name_list(self):
        return self.cg.get_exchanges_id_name_list()

    def get_price(self, ids, vs_currencies, include_market_cap=True, include_24hr_vol=True, include_24hr_change=True, include_last_updated_at=True):
        return self.cg.get_price(
            ids=ids,
            vs_currencies=vs_currencies,
            include_market_cap=include_market_cap,
            include_24hr_vol=include_24hr_vol,
            include_24hr_change=include_24hr_change,
            include_last_updated_at=include_last_updated_at
        )

    def get_coin_by_id(self, coin_id):
        return self.cg.get_coin_by_id(id=coin_id)

    def get_coin_ticker_by_id(self, coin_id):
        return self.cg.get_coin_ticker_by_id(id=coin_id)

    def get_coin_history_by_id(self, coin_id, date):
        return self.cg.get_coin_history_by_id(id=coin_id, date=date)

    def get_coin_market_chart_by_id(self, coin_id, vs_currency, days='max'):
        return self.cg.get_coin_market_chart_by_id(id=coin_id, vs_currency=vs_currency, days=days)

    def get_coin_market_chart_range_by_id(self, coin_id, vs_currency, from_timestamp, to_timestamp):
        return self.cg.get_coin_market_chart_range_by_id(
            id=coin_id,
            vs_currency=vs_currency,
            from_timestamp=from_timestamp,
            to_timestamp=to_timestamp
        )

    def get_coin_ohlc_by_id(self, coin_id, vs_currency, days=1):
        return self.cg.get_coin_ohlc_by_id(id=coin_id, vs_currency=vs_currency, days=days)

    def get_exchanges_by_id(self, exchange_id):
        return self.cg.get_exchanges_by_id(id=exchange_id)

    def get_exchanges_tickers_by_id(self, exchange_id):
        return self.cg.get_exchanges_tickers_by_id(id=exchange_id)

    def get_exchanges_volume_chart_by_id(self, exchange_id, days=7):
        return self.cg.get_exchanges_volume_chart_by_id(id=exchange_id, days=days)

    def get_exchange_rates(self):
        return self.cg.get_exchange_rates()

    def search(self, query):
        return self.cg.search(query=query)

    def get_search_trending(self):
        return self.cg.get_search_trending()

    def get_global(self):
        return self.cg.get_global()

    def get_global_defi(self):
        return self.cg.get_global_decentralized_finance_defi()

    def get_nfts_list(self):
        return self.cg.get_nfts_list()

    def get_nfts_by_id(self, nft_id):
        return self.cg.get_nfts_by_id(id=nft_id)

    def get_nfts_collection(self, asset_platform_id, contract_address):
        return self.cg.get_nfts_collection_by_asset_platform_id_and_contract_address(
            asset_platform_id=asset_platform_id,
            contract_address=contract_address
        )

    def get_derivatives(self):
        return self.cg.get_derivatives()

    def get_derivatives_exchanges(self):
        return self.cg.get_derivatives_exchanges()

    def get_derivatives_exchanges_by_id(self, exchange_id):
        return self.cg.get_derivatives_exchanges_by_id(id=exchange_id)

    def get_indexes(self):
        return self.cg.get_indexes()

    def get_indexes_list(self):
        return self.cg.get_indexes_list()

    def get_indexes_by_market_and_index(self, market_id, index_id):
        return self.cg.get_indexes_by_market_id_and_index_id(market_id=market_id, id=index_id)

    def get_companies_public_treasury(self, coin_id):
        return self.cg.get_companies_public_treasury_by_coin_id(coin_id=coin_id)

    def get_coin_market_summary(self, coin_id, vs_currency='usd'):
        data = self.cg.get_coin_by_id(id=coin_id)
        market_data = data.get('market_data', {})
        return {
            'current_price': market_data.get('current_price', {}).get(vs_currency),
            'market_cap': market_data.get('market_cap', {}).get(vs_currency),
            'price_change_24h': market_data.get('price_change_percentage_24h'),
            'high_24h': market_data.get('high_24h', {}).get(vs_currency),
            'low_24h': market_data.get('low_24h', {}).get(vs_currency)
        }

    def get_coin_price_change_percentage(self, coin_id, vs_currency='usd', days=7):
        chart = self.cg.get_coin_market_chart_by_id(id=coin_id, vs_currency=vs_currency, days=days)
        prices = chart.get('prices', [])
        if len(prices) >= 2:
            first = prices[0][1]
            last = prices[-1][1]
            change = ((last - first) / first) * 100
            return round(change, 2)
        return None

    def get_time_range(self, days=7):
        now = int(datetime.now().timestamp())
        then = now - days * 86400
        return then, now
