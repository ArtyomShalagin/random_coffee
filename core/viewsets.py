from django.http import HttpResponse
from rest_framework.views import APIView
import logging
import json
import core.telegram_api as tg


logger = logging.getLogger('general')


class TelegramHook(APIView):
    def post(self, request):
        # update = Update.de_json(request.data, bot())
        # webhook(update)

        json_msg = request.data
        # logger.info(json.dumps(json_msg, indent=4, sort_keys=True))
        print(json.dumps(json_msg, indent=4, sort_keys=True))
        update = tg.parse_update(json_msg)
        print()
        #
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
        #
        # if text is None:
        #     send_message(chat_id, 'Что-то пошло не так, в сообщении нет текста')
        # elif text == '/start':
        #     send_message(chat_id, 'Привет\n'
        #                           '/report - чтобы отчитаться\n'
        #                           '/skip - если не о чем отчитываться\n'
        #                           'Мы будем напоминать об отчетах по вечерам')
        # elif text == '/skip':
        #     TelegramHook.skip(employee)
        # elif text == '/report':
        #     TelegramHook.start_report(employee)
        # else:
        #     TelegramHook.handle_text(employee, text)
        #
        return HttpResponse('OK')