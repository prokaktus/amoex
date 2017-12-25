import asyncio

import aiohttp

from .base import BASE_URL


URL = 'iss/history/engines/stock/markets/shares/boards/'


_columns = ["BOARDID", "TRADEDATE", "SHORTNAME", "SECID",
            "NUMTRADES", "VALUE", "OPEN", "LOW", "HIGH",
            "LEGALCLOSEPRICE", "WAPRICE", "CLOSE", "VOLUME",
            "MARKETPRICE2", "MARKETPRICE3", "ADMITTEDQUOTE",
            "MP2VALTRD", "MARKETPRICE3TRADESVALUE", "ADMITTEDVALUE",
            "WAVAL"]
_columns_len = len(_columns)


class HistoryShares:
    
    def __init__(self, board='tqbr'):
        self.url = '{}{}{}/securities'.format(BASE_URL, 
            URL, board)

    async def call_chunks(self):
        pass

    async def get_securities(self, date=None):
        return await self.call(date=date)

    def _sync_wrapper(self, func, *args, **kwargs):
        # TODO: allow to customize loop
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(func(*args, **kwargs))

    def get_securities_sync(self, *args, **kwargs):
        return self._sync_wrapper(self.get_securities, *args, **kwargs)

    async def get_security(self, ticker, start_date=None, end_date=None):
        """
        Because MOEX api doesn't allow you to get single security data for
        specific time, we need to implement date range by ourselves
        """
        raise NotImplemented()

    @staticmethod
    def convert_response(payload):
        return {
            k: payload[i] for k, i in zip(_columns, range(_columsn_len))
        }

    @staticmethod
    def assert_reponse(response):
        # TODO: add error-checking and retry
        pass


    async def call(self, ticker=None, date=None):
        """
        Perform call to the API
        """
        url = '{}.json'.format(self.url)

        params = dict(**{'date': date} if date else {})

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                print(resp.status)
                return await resp.json()
