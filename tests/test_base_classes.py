import pytest
from LeBotTel.base_message_handler import BaseMessageHandler
from LeBotTel.base_telegram_bot import BaseTelegramBot
from LeBotTel.exceptions import ChatIdError
from conftest import FakeMessageHandler


def test_get_chat_id(mock_api, token, chat_id):
    mock_api.get(
        f"https://api.telegram.org/bot{token}/getUpdates",
        json={"result": [{"message": {"chat": {"id": chat_id}}}]},
    )
    bot = BaseTelegramBot(token)
    bot.get_chat_id()
    assert bot.chat_id == chat_id


def test_get_chat_id_error(mock_api, token):
    mock_api.get(f"https://api.telegram.org/bot{token}/getUpdates", json={"result": []})
    bot = BaseTelegramBot(token)
    with pytest.raises(ChatIdError):
        bot.get_chat_id()


def test_export_chat_id(chat_id, tmp_path):
    bot = BaseTelegramBot("token", chat_id)
    bot.export_chat_id(tmp_path / "chat.id")
    with open(tmp_path / "chat.id", "r") as f:
        assert f.read() == chat_id


def test_export_chat_id_error(chat_id):
    bot = BaseTelegramBot("token", chat_id)
    with pytest.raises(ChatIdError):
        bot.export_chat_id("/this/is/not/a/valid/path/chat.id")


def test_import_chat_id(chat_id, tmp_path):
    with open(tmp_path / "chat.id", "w") as f:
        f.write(chat_id)
    bot = BaseTelegramBot("token")
    bot.import_chat_id(tmp_path / "chat.id")
    assert bot.chat_id == chat_id


def test_import_chat_id_error():
    bot = BaseTelegramBot("token")
    with pytest.raises(ChatIdError):
        bot.import_chat_id("/this/is/not/a/valid/path/chat.id")


def test_send_message(mock_api, token, chat_id):
    mock_api.get(
        f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text=Hello+World",
        json={"result": "ok"},
    )
    bot = BaseTelegramBot(token, chat_id)
    response = bot.send_message("Hello World")
    assert response["result"] == "ok"


def test_send_message_error(token):
    bot = BaseTelegramBot(token)
    with pytest.raises(ChatIdError):
        bot.send_message("Hello World")


def test_send_image(mock_api, token, chat_id):
    mock_api.post(
        f"https://api.telegram.org/bot{token}/sendPhoto", json={"result": "ok"}
    )
    bot = BaseTelegramBot(token, chat_id)
    response = bot.send_image(b"Hello World")
    assert response["result"] == "ok"


def test_send_image_error(token):
    bot = BaseTelegramBot(token)
    with pytest.raises(ChatIdError):
        bot.send_image(b"Hello World")


def test_start_listener(mock_api, token, chat_id):
    mock_api.get(
        f"https://api.telegram.org/bot{token}/getUpdates",
        json={
            "result": [
                {"update_id": 2, "message": {"chat": {"id": chat_id}, "text": "test"}}
            ]
        },
    )
    bot = BaseTelegramBot(token, chat_id)
    handler = FakeMessageHandler(bot)
    bot.start_listener(handler)
    assert handler.test == True
    bot.running = False


def test_start_listener_error(token):
    bot = BaseTelegramBot(token)
    handler = FakeMessageHandler(bot)
    with pytest.raises(ChatIdError):
        bot.start_listener(handler)
