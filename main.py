import os
import uvicorn
import openpyxl

from dotenv import load_dotenv
from datetime import datetime

from fastapi import FastAPI, Request, HTTPException, Header

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent, BeaconEvent

from linebot.v3.messaging import (
    ApiClient, 
    MessagingApi, 
    Configuration, 
    ReplyMessageRequest, 
    TextMessage, 
    # FlexMessage, 
    # Emoji,
)


app = FastAPI()

load_dotenv(override=True)

# LINE Access Key
get_access_token = os.getenv('ACCESS_TOKEN')
configuration = Configuration(access_token=get_access_token)
# LINE Secret Key
get_channel_secret = os.getenv('CHANNEL_SECRET')
handler = WebhookHandler(channel_secret=get_channel_secret)

@app.post("/callback")
async def callback(request: Request, x_line_signature: str = Header(None)):
    body = await request.body()
    body_str = body.decode('utf-8')
    try:
        handler.handle(body_str, x_line_signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        raise HTTPException(status_code=400, detail="Invalid signature.")

    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event: MessageEvent):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        reply_message = "Hello from Dev Environment"    # เพิ่มเติมข้อความตรงนี้เพื่อตอบกลับ

        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_message)]
            )
        )

# @handler.add(BeaconEvent)
# def handle_beacon(event: BeaconEvent):
#     print(event)

#     user_id = event.source.user_id  ## รับ user_id จากคนที่เข้ามา
#     request_timestamp = event.timestamp  ## รับเวลาจากคนที่เข้ามา

#     file_path = "excel/data.xlsx"
#     workbook = openpyxl.load_workbook(file_path)
#     sheet = workbook.active

#     workbook = openpyxl.Workbook()
#     sheet = workbook.active

#     new_record = [f"{user_id}", f"{request_timestamp}"]   ## ข้อความที่จะเพิ่มเข้าไปใน Excel
#     sheet.append(new_record)
#     workbook.save(file_path)
#     print("Record added successfully!")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")