##################################################################################
#  You can add your actions in this file or create any other file in this folder #
##################################################################################

from rasa_sdk import Action
from rasa_sdk.events import SlotSet, ReminderScheduled, ConversationPaused, ConversationResumed, FollowupAction, Restarted, ReminderScheduled


class MyAction(Action):

    def name(self):
        return 'action_my_action'

    def run(self, dispatcher, tracker, domain):
        # do something.
        return []



class FetchStatus(Action):
    def name(self):
        return 'action_fetch_status'
    def run(self, dispatcher, tracker, domain):
        print('=========================== my actions ===========================')
        print("last tracker input", tracker.get_latest_input_channel())
        print("current state", tracker.current_state())
        print(dispatcher)
        print(tracker)
        print(domain)
        return []
