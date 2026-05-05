from fastapi import FastAPI, Request, Header

from linebot import LineBotApi, WebhookHandler

from linebot.models import MessageEvent, TextMessage, TextSendMessage

import os

app = FastAPI()

@app.get("/")
def home():
    return {"status": "ok", "service": "line-bot"}


@app.get("/health")
def health():
    return {"status": "ok"}


LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.post("/callback")

async def callback(request: Request, x_line_signature: str = Header(...)):

    body = await request.body()

    body = body.decode("utf-8")

    handler.handle(body, x_line_signature)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)

def handle_message(event):

    user_msg = event.message.text

    reply = f"你說的是：{user_msg}"

    line_bot_api.reply_message(

        event.reply_token,

        TextSendMessage(text=reply)

    )
 
