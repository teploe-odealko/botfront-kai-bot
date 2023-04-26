##################################################################################
#  You can add your actions in this file or create any other file in this folder #
##################################################################################
import asyncio
import os
from time import sleep

import httpx
print('httpx ver', httpx.__version__)
import datetime

from rasa_sdk import Action
from rasa_sdk.events import SlotSet, ReminderScheduled, ConversationPaused, ConversationResumed, FollowupAction, Restarted, ReminderScheduled
import sys
import telegram
from pymongo import MongoClient
import traceback
import logging

logger = logging.getLogger(__name__)


class MyActi(Action):

    def name(self):
        return 'action_unknown'

    def run(self, dispatcher, tracker, domain):
        # do something.
        try:

            print('action_unknown starting ...')
            current_state = tracker.current_state()
            telegram_metadata = current_state['latest_message']['metadata']

            print('telegram_metadata', telegram_metadata)
            if telegram_metadata['message_type'] == 'private':
                print('uttering utter_nlu_fallback', telegram_metadata)
    
                res = dispatcher.utter_message(template="utter_nlu_fallback")
                print('res uttering', res)
        except Exception as e:
            print('exception in action_unknown :', e)
        return []


def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = f'{os.getenv("MONGO_URL")}'

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['TelegramDB']



class FetchStatus(Action):
    def name(self):
        return 'action_fetch_status'

    def create_topic(self, tracker):
        print("create_topic")
        try:
            bot = telegram.Bot(os.getenv("BOT_TOKEN"))

            # await bot.send_message(text='Hi John!', chat_id=1234567890)
            chat_id = -1001943204451
            current_state = tracker.current_state()
            telegram_metadata = current_state['latest_message']['metadata']
            username = telegram_metadata['username']
            first_name = telegram_metadata['first_name']
            name = f'{first_name} / {username}'

            created_topic = bot.create_forum_topic(chat_id, name)
            dbname = get_database()
            collection_name = dbname["users1"]
            new_user = {
                "telegram_user_id": telegram_metadata['telegram_user_id'],
                "username": username,
                "first_name": first_name,
                "topic_id": created_topic['message_thread_id'],
                "admin_chat_id": chat_id,
                "user_chat_id": telegram_metadata['telegram_user_id'],
            }
            # bot.send_message(chat_id, str(new_user), reply_to_message_id=created_topic['message_thread_id'])
            events = current_state['events']
            print(events)
            print("event linst")
            x = collection_name.insert_one(new_user)

            print("telegram answer", name, created_topic, x.inserted_id, x.acknowledged)

            for event in events:
                print(event)
                while True:
                    try:
                        if 'event' in event and event['event'] == 'user':
                            bot.send_message(chat_id, event['text'], reply_to_message_id=created_topic['message_thread_id'], timeout=30)
                        elif 'event' in event and event['event'] == 'bot':
                            bot.send_message(chat_id, f">>BOT\n{event['text']}", reply_to_message_id=created_topic['message_thread_id'], timeout=30)
                        sleep(1)
                        break
                    except (telegram.error.TimedOut, telegram.error.RetryAfter) as exc:
                        logger.warning("!!!!!!!!!!!!!! EXCEPTION: !!!!!!!!!!!!!!!!!!!", exc, traceback.format_exc())
                        sleep(5)


        except Exception as exc:
            logger.error("!!!!!!!!!!!!!! EXCEPTION: !!!!!!!!!!!!!!!!!!!", exc, traceback.format_exc())

    def run(self, dispatcher, tracker, domain):
        logger.info('=========================== my actions ===========================')

        current_state = tracker.current_state()
        telegram_metadata = current_state['latest_message']['metadata']
        if telegram_metadata['message_type'] != 'private':
            return []

        dispatcher.utter_message(template="utter_to_human")
        self.create_topic(tracker)

        return []
