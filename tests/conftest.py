import pytest
import requests_mock

@pytest.fixture
def token():
    return "THIS_IS_A_VALID_TOKEN"

@pytest.fixture
def chat_id():
    return "THIS_IS_A_VALID_CHAT_ID"

@pytest.fixture
def mock_api():
    with requests_mock.Mocker() as m:
        yield m