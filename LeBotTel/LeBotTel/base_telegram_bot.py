import requests
from threading import Thread

from LeBotTel.base_message_handler import BaseMessageHandler
from LeBotTel.exceptions import ChatIdError, ListenerError



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
        self.running = True

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
    
    def start_listener(self, handler:BaseMessageHandler=None, timeout:int=30):
        """
        Start a listener for messages from the chat.
        This method is intended to be used in production.

        Parameters:
        timeout: int
            The timeout in seconds for long polling
        callback: function
            The callback function to call when a message is received
        """
        if self.chat_id is None:
            raise ChatIdError('chat_id is not set')
        if handler is None:
            handler = BaseMessageHandler(self)
        listener_thread = Thread(target=self._listen_for_messages, args=(handler, timeout), daemon=True)
        listener_thread.start() 


    def _listen_for_messages(self, handler:BaseMessageHandler, timeout:int=30):
        """
        Listen for messages from the chat. 
        This method is not intended to be used directly.
        Use start_listener instead, it will start this method in a new thread.

        Parameters:
        handler: BaseMessageHandler
            The handler to call when a message is received you can implement your own handler by inheriting from BaseMessageHandler
        timeout: int
            The timeout in seconds for long polling
        """
        latest_update_id = 0
        url = f'{self.base_url}getUpdates'
        while self.running: 
            try:
                response = requests.get(
                    url, 
                    {
                        'offset': latest_update_id+1,
                        'timeout': timeout,
                    }, 
                    timeout=timeout
                ) 
                data = response.json()
                if not data['result']:
                    continue
                for message in data['result']:
                    if message['update_id'] > latest_update_id:
                        latest_update_id = message['update_id']
                        handler.handle(message)
            except Exception as e:
                raise ListenerError('listener failed') from e
