from core.models import TelegramUpdate, TelegramMessage, TelegramUser, TelegramChat
import datetime
from random_coffee_bot.settings import BOT_TOKEN
import requests
import logging


logger = logging.getLogger("general")


def parse_update(update_json) -> TelegramUpdate:
    update_id = update_json["update_id"]
    if TelegramUpdate.objects.filter(update_id=update_id).exists():
        return TelegramUpdate.objects.get(update_id=update_id)
    message = None
    edited_message = None
    if "message" in update_json:
        message = parse_message(update_json["message"])
    if "edited_message" in update_json:
        edited_message = parse_message(update_json["edited_message"])
    effective_message = message or edited_message
    return TelegramUpdate.objects\
        .create(update_id=update_id, message=message, edited_message=edited_message,
                effective_message=effective_message,
                effective_chat=effective_message.chat if effective_message is not None else None,
                effective_user=effective_message.from_user if effective_message is not None else None)


def parse_message(message_json) -> TelegramMessage:
    message_id = message_json["message_id"]
    if TelegramMessage.objects.filter(message_id=message_id).exists():
        return TelegramMessage.objects.get(message_id=message_id)
    from_user = parse_user(message_json["from"])
    date = datetime.datetime.fromtimestamp(message_json["date"])
    chat = parse_chat(message_json["chat"])
    text = message_json["text"]
    return TelegramMessage.objects.create(message_id=message_id, from_user=from_user, date=date, chat=chat, text=text)


def parse_user(user_json) -> TelegramUser:
    uid = user_json["id"]
    if TelegramUser.objects.filter(uid=uid).exists():
        return TelegramUser.objects.get(uid=uid)  # TODO update user
    first_name = user_json["first_name"]
    last_name = user_json.get("last_name")
    username = user_json.get("username")
    return TelegramUser.objects.create(uid=uid, first_name=first_name, last_name=last_name, username=username)


def parse_chat(chat_json) -> TelegramChat:
    chat_id = chat_json["id"]
    if TelegramChat.objects.filter(chat_id=chat_id).exists():
        return TelegramChat.objects.get(chat_id=chat_id)  # TODO update chat
    first_name = chat_json.get("first_name")
    last_name = chat_json.get("last_name")
    username = chat_json.get("username")
    chat_type = chat_json["type"]
    title = chat_json.get("title")
    return TelegramChat.objects\
        .create(chat_id=chat_id, first_name=first_name, last_name=last_name, username=username,
                title=title, type=chat_type, state_updated=datetime.datetime.now())


def send_message(chat, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={chat.chat_id}&text={text}"
    try:
        logger.info(f"sending message to {chat}")
        requests.post(url)
    except Exception as e:
        logger.error(f"unable to send telegram message: {e}")
        # TODO handle blocked by user, retry to send before reporting etc
