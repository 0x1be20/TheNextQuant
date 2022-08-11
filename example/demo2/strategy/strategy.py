# -*- coding:utf-8 -*-

# 策略实现

import time
from quant import const
from quant.utils import tools
from quant.utils import logger
from quant.config import config
from quant.market import Market
from quant.trade import Trade as T
from quant.const import BINANCE_FUTURE
from quant.order import Order
from quant.market import Orderbook,Trade 
from quant.order import ORDER_ACTION_BUY, ORDER_STATUS_FAILED, ORDER_STATUS_CANCELED, ORDER_STATUS_FILLED


class MyStrategy:

    def __init__(self):
        """ 初始化
        """
        self.strategy = "my_strategy"
        self.platform = BINANCE_FUTURE
        self.account = config.accounts[0]["account"]
        self.access_key = config.accounts[0]["access_key"]
        self.secret_key = config.accounts[0]["secret_key"]
        self.symbol = config.symbol

        self.order_no = None  # 创建订单的id
        self.create_order_price = "0.0"  # 创建订单的价格

        # 交易模块
        cc = {
            "strategy": self.strategy,
            "platform": self.platform,
            "symbol": self.symbol,
            "account": self.account,
            "access_key": self.access_key,
            "secret_key": self.secret_key,
            "order_update_callback": self.on_event_order_update,
            "asset_update_callback":None,
            "position_update_callback":None,
            "init_success_callback":None,
        }
        self.trader = T(**cc)

        # 订阅行情
        Market(const.MARKET_TYPE_ORDERBOOK, const.BINANCE_FUTURE, self.symbol, self.on_event_orderbook_update)
        Market(const.MARKET_TYPE_TRADE, const.BINANCE_FUTURE, self.symbol, self.on_event_trade_update)

    async def on_event_orderbook_update(self, orderbook: Orderbook):
        """ 订单薄更新
        """
        # print("ok")
        # logger.info("orderbook:", orderbook, caller=self)
        logger.info("cost {}".format(time.time()-orderbook._eventtime))
        pass


    async def on_event_trade_update(self, trade: Trade):
        """ 交易更新
        """
        # logger.info("trade update:", trade, caller=self)
        logger.info("cost {}".format(time.time()-trade._eventtime))
        pass

    async def on_event_order_update(self, order: Order):
        """ 订单状态更新
        """
        logger.info("order update:", order, caller=self)

        # 如果订单失败、订单取消、订单完成交易
        if order.status in [ORDER_STATUS_FAILED, ORDER_STATUS_CANCELED, ORDER_STATUS_FILLED]:
            self.order_no = None


    async def on_position_update(self,position):
        logger.info('position {}',position)

    async def on_asset_update(self,asset):
        logger.info('asset {}',asset)


