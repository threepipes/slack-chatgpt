import json
import os
import traceback
from logging import getLogger
import urllib.request
import urllib.error

logger = getLogger(__name__)
url = os.getenv("SLACK_WEBHOOK_URL")


def slack(message):
    if url is None:
        return
    data = {
        "text": message,
    }
    headers = {"Content-Type": "application/json"}

    req = urllib.request.Request(url, json.dumps(data).encode("utf-8"), headers)
    try:
        with urllib.request.urlopen(req) as res:
            body = res.read()
    except:
        logger.error(traceback.format_exc())
        logger.error(f"Body: {body}")
