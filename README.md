Async MOEX Python API
========

**Work in progress. Library API could change significantly in future versions.**

Implemented only subset of MOEX API, because docs are very poor and I personally use only free features.

If you want more, please notify me about that or provide PRs!

### Installation

```
pip install amoex
```

### Usage example

```
from datetime import datetime
from amoex.shares import HistoryShares

hs = HistoryShares()
d = datetime.strptime('2018-01-03', '%Y-%m-%d')

data = hs.get_securities_sync(d)
data['SBER']

Out:
{'ADMITTEDQUOTE': 231.9,
 'ADMITTEDVALUE': 7965492945.5,
 'BOARDID': 'TQBR',
 'CLOSE': 231.9,
 'HIGH': 232.7,
 'LEGALCLOSEPRICE': 231.9,
 'LOW': 226.35,
 'MARKETPRICE2': 230.55,
 'MARKETPRICE3': 230.55,
 'MARKETPRICE3TRADESVALUE': 7965492945.5,
 'MP2VALTRD': 7965492945.5,
 'NUMTRADES': 40597,
 'OPEN': 226.88,
 'SECID': 'SBER',
 'SHORTNAME': 'Сбербанк',
 'TRADEDATE': '2018-01-03',
 'VALUE': 7965492945.5,
 'VOLUME': 34549620,
 'WAPRICE': 230.55,
 'WAVAL': None}
```

### Limitations

Python 3.5+

### Resources

Official reference: https://iss.moex.com/iss/reference/

Official examples and tutorials (2014 year): http://www.moex.com/a2193