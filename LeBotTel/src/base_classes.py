import requests

class ChatIdError(Exception):
    pass


class BaseTelegramBot:
    def __init__(self, token:str, chat_id:str=None) -> None:
        self.token = token
        self.chat_id = chat_id
        self.base_url = f'https://api.telegram.org/bot{self.token}/'

    def get_chat_id(self) -> None:
        url = f'{self.base_url}getUpdates'
        response = requests.get(url)
        data = response.json()
        try:
            self.chat_id = data['result'][0]['message']['chat']['id']
        except Exception as e:
            raise ChatIdError('chat_id not found') from e
        
    def export_chat_id(self, filename:str='chat.id') -> None:
        try:
            with open(filename, 'w') as f:
                f.write(self.chat_id)
        except Exception as e:
            raise ChatIdError(f'can not write to file {filename}') from e

    def import_chat_id(self, filename:str='chat.id') -> None:
        try:
            with open(filename, 'r') as f:
                self.chat_id = f.read()
        except Exception as e:
            raise ChatIdError(f'can not read from file {filename}') from e


    def send_message(self, message:str) -> dict:
        if self.chat_id is None:
            raise ChatIdError('chat_id is not set')
        url = f'{self.base_url}sendMessage?chat_id={self.chat_id}&text={message}'
        response = requests.get(url)
        return response.json()
    
    def send_image(self, image: bytes) -> dict:
        if self.chat_id is None:
            raise ChatIdError('chat_id is not set')
        url = f'{self.base_url}sendPhoto'
        files = {'photo': ("image.png", image, "image/png")}
        data = {'chat_id' : self.chat_id}
        response = requests.post(url, files=files, data=data)
        return response.json()
