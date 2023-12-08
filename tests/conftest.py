import pytest
from LeBotTel.base_message_handler import BaseMessageHandler
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

class FakeMessageHandler(BaseMessageHandler):
    def __init__(self, bot):
        super().__init__(bot)
        self.test = False

    def handle(self, message):
        if "test" in message["message"]["text"]:
            self.test = True


class FakeBot:
    def __init__(self):
        self.sent_messages = []

    def send_message(self, text):
        self.sent_messages.append(text)