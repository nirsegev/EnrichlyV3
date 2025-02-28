import os
import httpx
from config import get_settings

async def send_message_with_buttons(chat_id: int, text: str, buttons: dict):
    """Send a message with inline keyboard buttons."""
    settings = get_settings()
    url = settings.TELEGRAM_API_URL + "sendMessage"
    payload = {"chat_id": chat_id, "text": text, "reply_markup": buttons}

    print(
        "send message with buttons: ",
        text,
        " with buttons: ",
        buttons,
        " to chat: ",
        chat_id,
    )

    async with httpx.AsyncClient() as client:
        await client.post(url, json=payload)

async def send_message(chat_id: int, text: str):
    url = os.getenv("TELEGRAM_API_URL") + "sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    print("send message: ", text, " to chat: ", chat_id)
    
    async with httpx.AsyncClient() as client:
        await client.post(url, json=payload) 