import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('A0oH5TAmroWn0GpaOS5MmrE2su9SQQfp7TjgaSB2YxcTgBhMtR8UL7rJRE36ZxWUhYPFePp2NGgtwKdXVlRUpLO8qGpAc/A9GOoqEQUNek7MgLnZY+AmLEITE4DcUPGQOWbq7qXyJKsM3SQTxUyNiwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('935ed0d654f0ae4e4ab7d1a11ab1bacc')


@app.route("/callback", methods=['POST'])
def callback():
    # Get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # Get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # Handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
