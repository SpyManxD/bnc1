import logging
import time
from typing import List, Dict

from binance.client import Client
from binance.exceptions import BinanceAPIException

from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BotFunctions:
    def __init__(self, config: Config):
        self.client = Client(config.API_KEY, config.API_SECRET)
        self.config = config

    def get_balance(self, symbol: str) -> float:
        balance = self.client.get_asset_balance(asset=symbol)
        return float(balance['free'])

    def get_symbol_info(self, symbol: str) -> Dict:
        return self.client.get_symbol_info(symbol)

    def get_order_book(self, symbol: str, limit: int = 5) -> Dict:
        return self.client.get_order_book(symbol=symbol, limit=limit)

    def get_recent_trades(self, symbol: str, limit: int = 5) -> List[Dict]:
        return self.client.get_recent_trades(symbol=symbol, limit=limit)

    def get_klines(self, symbol: str, interval: str, limit: int = 5) -> List[List]:
        return self.client.get_klines(symbol=symbol, interval=interval, limit=limit)

    def create_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None) -> Dict:
        try:
            if order_type == 'LIMIT':
                order = self.client.create_order(
                    symbol=symbol,
                    side=side,
                    type=order_type,
                    timeInForce='GTC',
                    quantity=quantity,
                    price=str(price)
                )
            else:
                order = self.client.create_order(
                    symbol=symbol,
                    side=side,
                    type=order_type,
                    quantity=quantity
                )
            return order
        except BinanceAPIException as e:
            logger.error(f"An error occurred while creating the order: {e}")
            return None

    def cancel_order(self, symbol: str, order_id: str) -> Dict:
        try:
            result = self.client.cancel_order(symbol=symbol, orderId=order_id)
            return result
        except BinanceAPIException as e:
            logger.error(f"An error occurred while canceling the order: {e}")
            return None

    def get_open_orders(self, symbol: str) -> List[Dict]:
        return self.client.get_open_orders(symbol=symbol)

    def get_order(self, symbol: str, order_id: str) -> Dict:
        return self.client.get_order(symbol=symbol, orderId=order_id)

    def get_all_orders(self, symbol: str, limit: int = 5) -> List[Dict]:
        return self.client.get_all_orders(symbol=symbol, limit=limit)

        def get_account(self) -> Dict:
            return self.client.get_account()

    def get_exchange_info(self) -> Dict:
        return self.client.get_exchange_info()

    def get_ticker_price(self, symbol: str) -> Dict:
        return self.client.get_ticker_price(symbol=symbol)

    def get_ticker_24hr(self, symbol: str) -> Dict:
        return self.client.get_ticker_24hr(symbol=symbol)

    def get_historical_trades(self, symbol: str, limit: int = 5) -> List[Dict]:
        return self.client.get_historical_trades(symbol=symbol, limit=limit)

    def get_aggregate_trades(self, symbol: str, limit: int = 5) -> List[Dict]:
        return self.client.get_aggregate_trades(symbol=symbol, limit=limit)

    def get_avg_price(self, symbol: str) -> Dict:
        return self.client.get_avg_price(symbol=symbol)

    def get_depth(self, symbol: str, limit: int = 5) -> Dict:
        return self.client.get_depth(symbol=symbol, limit=limit)

    def ping(self) -> bool:
        return self.client.ping()

    def get_server_time(self) -> Dict:
        return self.client.get_server_time()

    def get_exchange_status(self) -> Dict:
        return self.client.get_system_status()

    def get_leverage(self, symbol: str) -> Dict:
        return self.client.futures_get_leverage(symbol=symbol)

    def set_leverage(self, symbol: str, leverage: int) -> Dict:
        return self.client.futures_change_leverage(symbol=symbol, leverage=leverage)

    def get_margin_type(self, symbol: str) -> Dict:
        return self.client.futures_get_margin_type(symbol=symbol)

    def set_margin_type(self, symbol: str, margin_type: str) -> Dict:
        return self.client.futures_change_margin_type(symbol=symbol, marginType=margin_type)

    def get_position_info(self, symbol: str) -> Dict:
        return self.client.futures_position_information(symbol=symbol)

    def get_income_history(self, symbol: str, income_type: str, limit: int = 5) -> List[Dict]:
        return self.client.futures_income_history(symbol=symbol, incomeType=income_type, limit=limit)

    def get_futures_ticker(self, symbol: str) -> Dict:
        return self.client.futures_ticker(symbol=symbol)

    def get_futures_orderbook_ticker(self, symbol: str) -> Dict:
        return self.client.futures_orderbook_ticker(symbol=symbol)

    def get_futures_liquidation_orders(self, symbol: str, limit: int = 5) -> List[Dict]:
        return self.client.futures_liquidation_orders(symbol=symbol, limit=limit)

    def get_futures_open_interest(self, symbol: str) -> Dict:
        return self.client.futures_open_interest(symbol=symbol)

    def get_futures_leverage_bracket(self, symbol: str) -> Dict:
        return self.client.futures_leverage_bracket(symbol=symbol)

    def get_futures_mark_price(self, symbol: str) -> Dict:
        return self.client.futures_mark_price(symbol=symbol)

    def get_futures_funding_rate(self, symbol: str) -> Dict:
        return self.client.futures_funding_rate(symbol=symbol)

    def get_futures_long_short_ratio(self, symbol: str) -> Dict:
        return self.client.futures_long_short_ratio(symbol=symbol)

        def get_futures_taker_buy_sell_ratio(self, symbol: str) -> Dict:
            return self.client.futures_taker_buy_sell_ratio(symbol=symbol)

    def get_futures_orderbook(self, symbol: str, limit: int = 5) -> Dict:
        return self.client.futures_orderbook(symbol=symbol, limit=limit)

    def get_futures_recent_trades(self, symbol: str, limit: int = 5) -> List[Dict]:
        return self.client.futures_recent_trades(symbol=symbol, limit=limit)

    def get_futures_historical_trades(self, symbol: str, limit: int = 5) -> List[Dict]:
        return self.client.futures_historical_trades(symbol=symbol, limit=limit)

    def get_futures_aggregate_trades(self, symbol: str, limit: int = 5) -> List[Dict]:
        return self.client.futures_aggregate_trades(symbol=symbol, limit=limit)

    def get_futures_klines(self, symbol: str, interval: str, limit: int = 5) -> List[Dict]:
        return self.client.futures_klines(symbol=symbol, interval=interval, limit=limit)

    def get_futures_continuous_klines(self, symbol: str, interval: str, limit: int = 5) -> List[Dict]:
        return self.client.futures_continuous_klines(symbol=symbol, interval=interval, limit=limit)

    def get_futures_index_price_klines(self, symbol: str, interval: str, limit: int = 5) -> List[Dict]:
        return self.client.futures_index_price_klines(symbol=symbol, interval=interval, limit=limit)

    def get_futures_mark_price_klines(self, symbol: str, interval: str, limit: int = 5) -> List[Dict]:
        return self.client.futures_mark_price_klines(symbol=symbol, interval=interval, limit=limit)

    def get_futures_margin_data(self, symbol: str) -> Dict:
        return self.client.futures_margin_data(symbol=symbol)

    def get_futures_position_margin_history(self, symbol: str, limit: int = 5) -> List[Dict]:
        return self.client.futures_position_margin_history(symbol=symbol, limit=limit)

    def get_futures_account_balance(self) -> List[Dict]:
        return self.client.futures_account_balance()

    def get_futures_account(self) -> Dict:
        return self.client.futures_account()

    def get_futures_position_risk(self) -> List[Dict]:
        return self.client.futures_position_risk()

    def get_futures_trade_list(self, symbol: str, limit: int = 5) -> List[Dict]:
        return self.client.futures_trade_list(symbol=symbol, limit=limit)

    def get_futures_income_history(self, symbol: str, limit: int = 5) -> List[Dict]:
        return self.client.futures_income_history(symbol=symbol, limit=limit)

    def get_futures_leverage_bracket(self) -> List[Dict]:
        return self.client.futures_leverage_bracket()

    def get_futures_adl_quantile(self, symbol: str) -> Dict:
        return self.client.futures_adl_quantile(symbol=symbol)

    def get_futures_api_trading_status(self) -> Dict:
        return self.client.futures_api_trading_status()

    def get_futures_data_stream(self) -> Dict:
        return self.client.futures_data_stream()

    def get_futures_symbol_orderbook_ticker(self, symbol: str) -> Dict:
        return self.client.futures_symbol_orderbook_ticker(symbol=symbol)

    def get_futures_symbol_price_ticker(self, symbol: str) -> Dict:
        return self.client.futures_symbol_price_ticker(symbol=symbol)

    def get_futures_symbol_order_list(self, symbol: str) -> Dict:
        return self.client.futures_symbol_order_list(symbol=symbol)

    def get_futures_all_orders(self, symbol: str) -> List[Dict]:
        return self.client.futures_all_orders(symbol=symbol)

    def get_futures_open_orders(self, symbol: str) -> List[Dict]:
        return self.client.futures_open_orders(symbol=symbol)

    def get_futures_open_order(self, symbol: str, orderId: str) -> Dict:
        return self.client.futures_get_order(symbol=symbol, orderId=orderId)

        def create_futures_order(self, symbol: str, side: str, type: str, quantity: float, price: float = None,
                                 timeInForce: str = None, newClientOrderId: str = None, stopPrice: float = None,
                                 icebergQty: float = None, newOrderRespType: str = 'RESULT') -> Dict:
            return self.client.futures_create_order(symbol=symbol, side=side, type=type, quantity=quantity, price=price,
                                                    timeInForce=timeInForce, newClientOrderId=newClientOrderId,
                                                    stopPrice=stopPrice, icebergQty=icebergQty,
                                                    newOrderRespType=newOrderRespType)

    def cancel_futures_order(self, symbol: str, orderId: str = None, origClientOrderId: str = None) -> Dict:
        return self.client.futures_cancel_order(symbol=symbol, orderId=orderId, origClientOrderId=origClientOrderId)

    def cancel_all_futures_open_orders(self, symbol: str) -> Dict:
        return self.client.futures_cancel_all_open_orders(symbol=symbol)

    def cancel_futures_open_orders(self, symbol: str) -> Dict:
        return self.client.futures_cancel_open_orders(symbol=symbol)

    def change_futures_margin_type(self, symbol: str, marginType: str) -> Dict:
        return self.client.futures_change_margin_type(symbol=symbol, marginType=marginType)

    def change_futures_leverage(self, symbol: str, leverage: int) -> Dict:
        return self.client.futures_change_leverage(symbol=symbol, leverage=leverage)

    def change_futures_position_margin(self, symbol: str, amount: float, type: int) -> Dict:
        return self.client.futures_change_position_margin(symbol=symbol, amount=amount, type=type)

    def create_futures_data_stream(self) -> Dict:
        return self.client.futures_create_data_stream()

    def keepalive_futures_data_stream(self, listenKey: str) -> Dict:
        return self.client.futures_keepalive_data_stream(listenKey=listenKey)

    def close_futures_data_stream(self, listenKey: str) -> Dict:
        return self.client.futures_close_data_stream(listenKey=listenKey)

    def get_futures_ping(self) -> Dict:
        return self.client.futures_ping()

    def get_futures_time(self) -> Dict:
        return self.client.futures_time()

    def get_futures_exchange_info(self) -> Dict:
        return self.client.futures_exchange_info()

    def get_futures_system_status(self) -> Dict:
        return self.client.futures_system_status()

    def get_futures_account_status(self) -> Dict:
        return self.client.futures_account_status()

    def get_futures_api_permissions(self) -> Dict:
        return self.client.futures_api_permissions()

        def get_futures_account(self) -> Dict:
            return self.client.futures_account()

    def get_futures_account_balance(self) -> Dict:
        return self.client.futures_account_balance()

    def get_futures_trade_fee(self) -> Dict:
        return self.client.futures_trade_fee()

    def get_futures_position_margin_history(self, symbol: str, type: int = None, startTime: int = None,
                                            endTime: int = None, limit: int = None) -> Dict:
        return self.client.futures_position_margin_history(symbol=symbol, type=type, startTime=startTime,
                                                           endTime=endTime, limit=limit)

    def get_futures_income_history(self, symbol: str = None, incomeType: str = None, startTime: int = None,
                                   endTime: int = None, limit: int = None, archived: str = None) -> Dict:
        return self.client.futures_income_history(symbol=symbol, incomeType=incomeType, startTime=startTime,
                                                  endTime=endTime, limit=limit, archived=archived)

    def get_futures_leverage_bracket(self, symbol: str = None) -> Dict:
        return self.client.futures_leverage_bracket(symbol=symbol)

    def get_futures_adl_quantile(self, symbol: str) -> Dict:
        return self.client.futures_adl_quantile(symbol=symbol)

    def get_futures_notional_and_leverage_brackets(self) -> Dict:
        return self.client.futures_notional_and_leverage_brackets()

    def get_futures_user_trades(self, symbol: str, startTime: int = None, endTime: int = None, limit: int = None,
                                fromId: int = None) -> Dict:
        return self.client.futures_user_trades(symbol=symbol, startTime=startTime, endTime=endTime, limit=limit,
                                               fromId=fromId)

    def get_futures_data_stream(self, listenKey: str) -> Dict:
        return self.client.futures_data_stream(listenKey=listenKey)

    def get_futures_mark_price(self, symbol: str = None) -> Dict:
        return self.client.futures_mark_price(symbol=symbol)

    def get_futures_funding_rate(self, symbol: str, startTime: int = None, endTime: int = None, limit: int = None) -> Dict:
        return self.client.futures_funding_rate(symbol=symbol, startTime=startTime, endTime=endTime, limit=limit)

    def get_futures_ticker(self, symbol: str) -> Dict:
        return self.client.futures_ticker(symbol=symbol)

    def get_futures_orderbook_ticker(self, symbol: str) -> Dict:
        return self.client.futures_orderbook_ticker(symbol=symbol)

    def get_futures_liquidation_orders(self, symbol: str = None, startTime: int = None, endTime: int = None,
                                       limit: int = None) -> Dict:
        return self.client.futures_liquidation_orders(symbol=symbol, startTime=startTime, endTime=endTime, limit=limit)

    def get_futures_open_interest(self, symbol: str) -> Dict:
        return self.client.futures_open_interest(symbol=symbol)

    def get_futures_position_risk(self) -> Dict:
        return self.client.futures_position_risk()

    def get_futures_account_trades(self, symbol: str, startTime: int = None, endTime: int = None, limit: int = None,
                                   fromId: int = None) -> Dict:
        return self.client.futures_account_trades(symbol=symbol, startTime=startTime, endTime=endTime, limit=limit,
                                                  fromId=fromId)
