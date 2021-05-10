import os
import json

import pytest
from asynctest import CoroutineMock, patch


@pytest.fixture
def securities_dummy_data():
    path = os.path.join(
        os.path.dirname(__file__),
        "testdata",
        "securities.json"
    )
    with open(path) as f:
        return json.load(f)


@pytest.fixture
def securities_empty_data():
    return {}


@pytest.fixture
def make_mock_response():
    """
    Factory for putting data into mocked response.

    Details:
    https://stackoverflow.com/a/48762969/1096846
    """

    def factory(mock_get, *items):
        mock_get.return_value.__aenter__.return_value.json = CoroutineMock(
            side_effect=items
        )

    return factory
