from datetime import datetime

from amoex.shares import HistoryShares
from asynctest import CoroutineMock, patch

TOTAL_SECURITIES = 100


@patch("aiohttp.ClientSession.get")
async def test_get_securities(mock_get, make_mock_response, securities_dummy_data, securities_empty_data):
    """
    Test basic logic with fetching all securities.
    """
    ticker = "AFLT"
    hs = HistoryShares()
    make_mock_response(mock_get, securities_dummy_data, securities_empty_data)

    resp = await hs.get_securities()

    assert resp
    assert len(resp) == TOTAL_SECURITIES
    security_data = resp[ticker]
    assert security_data
    assert security_data["SECID"] == ticker
    assert security_data["OPEN"] == 65.5
    assert security_data["CLOSE"] == 65.64
    assert security_data["SHORTNAME"] == "Аэрофлот"
    assert security_data["VOLUME"] == 6330320
