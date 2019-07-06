from django.http import HttpResponse
from rest_framework.views import APIView
import logging
import json
import core.telegram_api as tg
from core.models import *


logger = logging.getLogger('general')


def ensure_user_exists(tg_user):
    if not RCUser.objects.filter(telegram_uid=tg_user.uid).exists():
        RCUser.objects.create(telegram_user=tg_user, telegram_uid=tg_user.uid)


class TelegramHook(APIView):
    def post(self, request):
        json_data = request.data
        logger.info(json.dumps(json_data, indent=4, sort_keys=True))
        update = tg.parse_update(json_data)
        ensure_user_exists(update.effective_user)

        tg.send_message(update.effective_chat, "Мы пилим, скоро допилим, правда-правда")

        # if 'message' not in json_message:
        #     logger.info('no message field in message!')
        #     return
        #
        # msg = json_message['message']
        #
        # if msg.get('chat', {}).get('type') != 'private':
        #     return HttpResponse('OK') # TODO ensure chat exists first
        #
        # chat = TelegramHook._ensure_chat_exists(msg)
        # employee = TelegramHook._ensure_employee_exists(msg, chat)
        # chat_id = chat.chat_id
        # text = msg.get('text')
        return HttpResponse('OK')