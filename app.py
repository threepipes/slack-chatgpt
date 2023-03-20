import os
import re
from logging import basicConfig, INFO, getLogger

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

import chatgpt
import notification

logger = getLogger(__name__)


# Install the Slack app and get xoxb- token in advance
app = App(token=os.environ["SLACK_BOT_TOKEN"])


@app.message(":wave:")
def say_hello(message, say):
    user = message["user"]
    say(f"Hi there, <@{user}>!")


@app.event("app_mention")
def handle_mention(body, say):
    user = body["event"]["user"]
    message = body["event"]["text"]
    prompt = re.sub("(?:\s)<@[^, ]*|(?:^)<@[^, ]*", "", message)
    try:
        res = chatgpt.ask(prompt)
        say(f"<@{user}> {res}")
    except:
        say("I'm sorry, but I failed to ask ChatGPT for some reason.")
        raise


@app.event("message")
def handle_message_events(body, logger):
    logger.debug(body)


@app.error
def handle_error(error, body, logger):
    logger.exception(f"Error: {error}")
    logger.info(f"Request body: {body}")
    notification.slack(f"An error occured:\n{error}")


def loggingSettings():
    fmt = "%(asctime)s %(message)s"
    basicConfig(level=INFO, filename="./app.log", format=fmt)


if __name__ == "__main__":
    loggingSettings()
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()
