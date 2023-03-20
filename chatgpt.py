import asyncio
from chatgpt_wrapper.openai.api import OpenAIAPI


def ask(message: str) -> str:
    bot = OpenAIAPI()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop=loop)
    try:
        success, response, message = bot.ask(message)
        if success:
            return response
        else:
            raise RuntimeError(message)
    finally:
        asyncio.set_event_loop(None)


def ask_stream(message: str) -> str:
    bot = OpenAIAPI()
    text = ""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop=loop)
    try:
        for c in bot.ask_stream(message):
            if type(c) == str and c.endswith("\n"):
                yield text + c
                text = ""
            else:
                text += c
        if text != "":
            yield text
    finally:
        asyncio.set_event_loop(None)
