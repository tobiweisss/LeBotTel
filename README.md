![Logo](https://raw.githubusercontent.com/tobiweisss/LeBotTel/main/images/logo_text_inv.png#gh-dark-mode-only)
![Logo](https://raw.githubusercontent.com/tobiweisss/LeBotTel/main/images/logo_text.png#gh-light-mode-only)
## Abstract
LeBotTel is an easy to use python package to create your own Telegram bots for different use cases. For details how to use this package refer to the [quick start](#quick-start) section. 

## Name
The name LeBotTel is combined from "LeCun", "RoBot" and "Telegram". The "Le" in the name comes from Yann LeCun, to honor his work on neural networks (has nothing to do with this project, but he is a great scientist and pioneer in the field of neural networks (LeNet)). What has this bot to do with neural networks? We want to use this bot to log the training of neural networks. "Bot" comes from RoBot, because this is what the goal of this project is. And "Tel" comes from Telegram, because its a bot for Telegram. The "Pi" in our logo represents looks similar to the "tT" in "LeBotTel" and stands for the used Programming Language Python.

## Quick Start

#### Installation

```bash
pip install LeBotTel
```

#### Send a message

```python
from LeBotTel import BaseTelegramBot

bot = BaseTelegramBot(token="YOUR_BOT_TOKEN", chat_id="YOUR_CHAT_ID")

bot.send_message("Hello World!") # Raises ChatIdError if chat_id is not set
```

<b>Hint:</b> To get the `chat_id` you first have to send your Bot a message (e.g. `/start`). Then you need to send a `GET` request to the following URL: 

`https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`

In the returned JSON you will find the `chat_id` under `message`->`chat`->`id`.

#### Send an image

```python
from LeBotTel.base_telegram_bot import BaseTelegramBot
import imageio
import io

bot = BaseTelegramBot(token="YOUR_BOT_TOKEN", chat_id="YOUR_CHAT_ID")

buffer = io.BytesIO()
img = imageio.imread('PATH_TO_IMAGE') # Image has to be in *.png format
imageio.imsave(buffer, img, format="PNG")

bot.send_image(buffer.getvalue()) # Raises ChatIdError if chat_id is not set
```

#### Send a gif

```python
from LeBotTel.base_telegram_bot import BaseTelegramBot
import imageio
import io
import glob

bot = BaseTelegramBot(token="YOUR_BOT_TOKEN", chat_id="YOUR_CHAT_ID")

buffer = io.BytesIO()
images = []
image_files = glob.glob('PATH_TO_IMAGES_DIR/*.png') # Images have to be in *.png format

for image_file in image_files:
    images.append(imageio.imread(image_file))

imageio.mimsave(buffer, images, format="GIF", duration=30)

bot.send_gif(buffer.getvalue()) # Raises ChatIdError if chat_id is not set
```


## Changelog
- 0.1.0: setup package. Bot can send messages and images
- 0.2.0: Bot can receive messages 
- 0.3.0: Add method `export_config` to save the current token and chat_id to a file, add classmethod `from_config` to create a bot from the config file, add classmethod `from_env` to create a bot from the environment variables `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`. Methods `import_chat_id` and `export_chat_id` are deprecated and will be removed in version 1.0.0
- 0.3.1: Adapting package structure 
- 0.4.0: Add `send_gif` method
- 0.4.1: Switch to pyproject.toml for build

## Authors
- Antonio Vidos
- Tobias Lettner
- Tobias Weiß
- Uwe Kölbel
