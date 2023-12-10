from LeBotTel.base_message_handler import BaseMessageHandler
from conftest import FakeBot


def test_handle_help():
    bot = FakeBot()
    handler = BaseMessageHandler(bot)
    message = {"message": {"text": "/help"}}
    handler.handle(message)
    assert bot.sent_messages == [handler.help()]


def test_handle_hello():
    bot = FakeBot()
    handler = BaseMessageHandler(bot)
    message = {"message": {"text": "Hello", "from": {"first_name": "John"}}}
    handler.handle(message)
    assert bot.sent_messages == ["Hello John!"]


def hanlde_question():
    bot = FakeBot()
    handler = BaseMessageHandler(bot)
    message = {"message": {"text": "?"}}
    handler.handle(message)
    assert bot.sent_messages == [
        "The answer to life, the universe and everything is 42."
    ]
