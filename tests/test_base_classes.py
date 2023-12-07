import pytest
from LeBotTel.base_classes import BaseTelegramBot
from LeBotTel.exceptions import ChatIdError


def test_get_chat_id(mock_api, token, chat_id):
    mock_api.get(f'https://api.telegram.org/bot{token}/getUpdates', json={'result': [{'message': {'chat': {'id': chat_id}}}]} )
    bot = BaseTelegramBot(token)
    bot.get_chat_id()
    assert bot.chat_id == chat_id

def test_get_chat_id_error(mock_api, token):
    mock_api.get(f'https://api.telegram.org/bot{token}/getUpdates', json={'result': []} )
    bot = BaseTelegramBot(token)
    with pytest.raises(ChatIdError):
        bot.get_chat_id()

def test_export_chat_id(chat_id, tmp_path):
    bot = BaseTelegramBot('token', chat_id)
    bot.export_chat_id(tmp_path / 'chat.id')
    with open(tmp_path / 'chat.id', 'r') as f:
        assert f.read() == chat_id

def test_export_chat_id_error(chat_id, tmp_path):
    bot = BaseTelegramBot('token', chat_id)
    with pytest.raises(ChatIdError):
        bot.export_chat_id('/this/is/not/a/valid/path/chat.id')

def test_import_chat_id(chat_id, tmp_path):
    with open(tmp_path / 'chat.id', 'w') as f:
        f.write(chat_id)
    bot = BaseTelegramBot('token')
    bot.import_chat_id(tmp_path / 'chat.id')
    assert bot.chat_id == chat_id

def test_import_chat_id_error(chat_id, tmp_path):
    bot = BaseTelegramBot('token')
    with pytest.raises(ChatIdError):
        bot.import_chat_id('/this/is/not/a/valid/path/chat.id')



