class BaseMessageHandler:
    """
    Base class for message handlers.
    Feel free to add your own message handlers by inheriting from this class.
    Your own message handler should implement the handle method and the help method.
    """

    def __init__(self, bot):
        """
        Initialize the message handler.
        """
        self.bot = bot

    def handle(self, message):
        """
        Handle a message from the chat.
        This method should be implemented by your own message handler.

        Parameters:
        message: dict
            The message to handle
        """
        if "/help" in message["message"]["text"]:
            return self.bot.send_message(self.help())
        elif "Hello" in message["message"]["text"]:
            return self.bot.send_message(
                f"Hello {message['message']['from']['first_name']}!"
            )
        elif "?" in message["message"]["text"]:
            return self.bot.send_message(
                "The answer to life, the universe and everything is 42."
            )

    def help(self):
        """
        Return a help message.
        This method should be implemented by your own message handler.

        Returns:
            str: the help message
        """
        return (
            "Welcome to the LeBotTel help page.\n\n"
            + "Following commands are available:\n"
            + "/help - Show this help message\n"
            + "Hello - Bot will greet you\n"
            + "? - Bot will tell you the answer to life, the universe and everything"
        )
