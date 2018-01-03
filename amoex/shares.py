import asyncio
from datetime import datetime, date as date_type

import aiohttp
from toolz import merge

from .base import BASE_URL


URL = 'iss/history/engines/stock/markets/shares/boards/'
PAGE_SIZE = 100


_columns = ["BOARDID", "TRADEDATE", "SHORTNAME", "SECID",
            "NUMTRADES", "VALUE", "OPEN", "LOW", "HIGH",
            "LEGALCLOSEPRICE", "WAPRICE", "CLOSE", "VOLUME",
            "MARKETPRICE2", "MARKETPRICE3", "ADMITTEDQUOTE",
            "MP2VALTRD", "MARKETPRICE3TRADESVALUE", "ADMITTEDVALUE",
            "WAVAL"]
_columns_len = len(_columns)


class HistoryShares:
    DATE_FORMAT = '%Y-%m-%d'
    
    def __init__(self, board='tqbr', loop=None):
        self.url = '{}{}{}/securities'.format(BASE_URL, 
            URL, board)
        self.loop = loop or asyncio.get_event_loop()

    def _sync_wrapper(self, func, *args, **kwargs):
        return self.loop.run_until_complete(func(*args, **kwargs))

    @classmethod
    def _serialize_date(cls, date):
        """
        Convert date to string representation (if required)
        """
        if isinstance(date, (datetime, date_type, )):
            return date.strftime(cls.DATE_FORMAT)
        return date

    @classmethod
    def _parse_date(cls, date_str):
        return datetime.strptime(date_str, cls.DATE_FORMAT).date()

    async def get_securities(self, date=None):
        data = []
        start = 0
        while True:
            page_data = await self.call(date=date, start=start)
            if not page_data:
                break
            data.extend(page_data)
            start += PAGE_SIZE

        return {d['SECID']: d for d in data}

    def get_securities_sync(self, *args, **kwargs):
        return self._sync_wrapper(self.get_securities, *args, **kwargs)

    async def get_security(self, ticker, start_date=None, end_date=None):
        """
        Because MOEX api doesn't allow you to get single security data for
        specific time, we need to implement date range by ourselves
        """
        # docs https://iss.moex.com/iss/reference/13 doesn't provide info on 
        # that
        start = 0

        url = '{}/{}'.format(self.url, ticker)
        data = {}
        start_date = self._serialize_date(start_date)
        end_date = self._serialize_date(end_date)

        while True:
            page_data = await self.call(ticker, url, start=start)
            if not page_data:
                break
            last_entry = page_data[-1]
            if start_date and start_date > last_entry['TRADEDATE']:
                start += PAGE_SIZE
                continue
            first_entry = page_data[0]
            if end_date and end_date < first_entry['TRADEDATE']:
                break

            for d in page_data:
                trade_date = d['TRADEDATE']
                if (not start_date or start_date < trade_date) and \
                   (not end_date or trade_date < end_date):
                    data[self._parse_date(trade_date)] = d

            start += PAGE_SIZE

        return data

    def get_security_sync(self, *args, **kwargs):
        return self._sync_wrapper(self.get_security, *args, **kwargs)

    @staticmethod
    def convert_response(payload):
        data = payload.get('history', {}).get('data', {})
        for d in data:
            yield {
                k: d[i] for k, i in zip(_columns, range(_columns_len))
            }

    @staticmethod
    def assert_reponse(response):
        # TODO: add error-checking and retry
        pass


    async def call(self, ticker=None, url=None, date=None, start=None):
        """
        Perform call to the API
        """
        url = '{}.json'.format(url or self.url)
        date = self._serialize_date(date)

        params = merge(
            {'date': date} if date else {},
            {'start': start} if start else {}
        )

        async with aiohttp.ClientSession(raise_for_status=True) as session:
            async with session.get(url, params=params) as resp:
                payload = await resp.json()
                data = list(self.convert_response(payload))
                return data
