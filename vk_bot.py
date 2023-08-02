import random
import logging

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from environs import Env
from openpyxl import load_workbook

from telegram_logging import TgLogsHandler

logger = logging.getLogger('vk-dialogflow-bot')


def load_faq(filename):
    faq_file = load_workbook(filename=filename)
    faq_data = faq_file.worksheets[0]
    faq = []
    for row in faq_data.values:
        faq.append(
            {
                'question': row[0],
                'answer': row[1],
                'similarity': 0
            }
        )
    return faq


def make_ngrams(text, n_length=4):
    text_length = len(text)
    start = 0
    limit = n_length
    ngrams = []
    while limit <= text_length:
        ngrams.append(text[start:limit].lower())
        start += 1
        limit += 1
    return ngrams


def calculate_similarity(text_one, text_two):
    set_one = set(make_ngrams(text_one))
    set_two = set(make_ngrams(text_two))
    similar = set_one.intersection(set_two)
    percentage_one = len(similar) / len(set_one)
    percentage_two = len(similar) / len(set_two)
    return percentage_one * percentage_two


def reply_to_message(faq, event, vk_api):
    user_message = event.message
    for question in faq:
        question['similarity'] = calculate_similarity(
            question['question'],
            user_message
        )
    faq = [question for question in faq if question['similarity'] > 0]
    faq.sort(key=lambda question: question['similarity'], reverse=True)
    most_relevant = faq[:3]

    if most_relevant:
        basic_message = '\n'.join(
            [
                'Ваш вопрос похож на следующие вопросы.',
                'Возможно, ответ на один из них вам подойдет?'
            ]
        )
        questions = [
            f'Вопрос: {question["question"]}\nОтвет: {question["answer"]}' for question in most_relevant
        ]
        final_message = basic_message + '\n' + '\n'.join(questions)
    else:
        final_message = '''Ваш вопрос передан организаторам, они ответят вам при первой же возможности.'''
    vk_api.messages.send(
        user_id=event.user_id,
        message=final_message,
        random_id=random.randint(1, 1000)
    )


if __name__ == '__main__':
    env = Env()
    env.read_env()
    vk_group_token = env('VK_GROUP_TOKEN')
    tg_log_chat_id = env('TG_LOG_CHAT_ID')
    tg_api_token = env('TG_API_KEY')

    handler = TgLogsHandler(tg_api_token, tg_log_chat_id)
    handler.setFormatter(
        logging.Formatter('%(process)d %(levelname)s %(message)s')
    )
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    faq = load_faq('faq.xlsx')

    vk_session = vk.VkApi(token=vk_group_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    logger.info('Bot started')
    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    reply_to_message(faq, event, vk_api)
        except Exception as ex:
            logger.exception(ex)
