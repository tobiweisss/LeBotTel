import requests
from .exceptions import ChatIdError



class BaseTelegramBot:
    """
    This is a base class for telegram bots.
    It is not intended to be used directly.
    """
    def __init__(self, token:str, chat_id:str=None) -> None:
        """
        Parameters:
        token: str
            The token of the bot
        chat_id: str
            The chat_id of the chat to send messages to
        """
        self.token = token
        self.chat_id = chat_id
        self.base_url = f'https://api.telegram.org/bot{self.token}/'

    def get_chat_id(self) -> None:
        """
        Get the chat_id of the chat to send messages to.

        Raises:
            ChatIdError: if the chat_id can not be found
        """
        url = f'{self.base_url}getUpdates'
        response = requests.get(url)
        data = response.json()
        try:
            self.chat_id = data['result'][0]['message']['chat']['id']
        except Exception as e:
            raise ChatIdError('chat_id not found') from e
        
    def export_chat_id(self, filename:str='chat.id') -> None:
        """
        Save the current chat_id to a file.

        Parameters:
        filename: str
            The filename to save the chat_id to (default: 'chat.id')
        
        Raises:
            ChatIdError: if the chat_id can not be saved to the file
        """
        try:
            with open(filename, 'w') as f:
                f.write(str(self.chat_id))
        except Exception as e:
            raise ChatIdError(f'can not write to file {filename}') from e

    def import_chat_id(self, filename:str='chat.id') -> None:
        """
        Load the chat_id from a file.

        Parameters:
        filename: str
            The filename to load the chat_id from (default: 'chat.id')
        
        Raises:
            ChatIdError: if the chat_id can not be loaded from the file
        """
        try:
            with open(filename, 'r') as f:
                self.chat_id = f.read()
        except Exception as e:
            raise ChatIdError(f'can not read from file {filename}') from e


    def send_message(self, message:str) -> dict:
        """
        Send a text message to the chat.

        Parameters:
        message: str
            The message to send
        
        Raises:
            ChatIdError: if the chat_id is not set

        Returns:
            dict: the response from the telegram api
        """
        if self.chat_id is None:
            raise ChatIdError('chat_id is not set')
        url = f'{self.base_url}sendMessage?chat_id={self.chat_id}&text={message}'
        response = requests.get(url)
        return response.json()
    
    def send_image(self, image: bytes) -> dict:
        """
        Send a image to the chat.

        Parameters:
        image: bytes
            The image to send (png)
        
        Raises:
            ChatIdError: if the chat_id is not set
        
        Returns:
            dict: the response from the telegram api
        """
        if self.chat_id is None:
            raise ChatIdError('chat_id is not set')
        url = f'{self.base_url}sendPhoto'
        files = {'photo': ("image.png", image, "image/png")}
        data = {'chat_id' : self.chat_id}
        response = requests.post(url, files=files, data=data)
        return response.json()
