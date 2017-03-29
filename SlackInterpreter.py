#
# Cole Smith
# Event Reminder for Tech@NYU
# SlackInterpreter.py
#

import os
from slackclient import SlackClient


class SlackInterpreter(object):

    def __init__(self):
        # CRITICAL: THIS IS SLACK BACK'S THIS WILL NEED TO CHANGE
        self.BOT_ID = "U2JAPPT8R"
        self.API_TOKEN = os.environ["SLACK_ER_BOT_TOKEN"]
        self.slack_client = SlackClient(self.API_TOKEN)

    def connect(self):
        """
        Attempts connection to the Slack Channel using the given
        API Token and Bot ID
        :return: None
        """
        if self.slack_client.rtm_connect():
            print("Event Reminders connected and running!")
        else:
            print("Connection failed. Invalid Slack token or bot ID?")

    def find_user_by_full_name(self, first_name, last_name):
        """
        Searches Slack for a user's username given their full name
        :param first_name: String
        :param last_name: String
        :return: String, User's Slack username
        """
        users_list = self.slack_client.api_call("users.list")
        if users_list["ok"]:
            for user in users_list["members"]:
                try:
                    if str(user["profile"]["first_name"]).lower() == first_name.lower() and \
                       str(user["profile"]["last_name"]).lower() == last_name.lower():
                        return user["name"]
                except KeyError:
                    continue

    def send_message_to_user(self, username, message):
        """
        Sends a user a message on Slack
        :param username: String, Slack username
        :param message: String, message
        :return: None
        """
        if not username:
            print "[ WRN ] Trying to send DM to null user"
        else:
            channel = "@" + username
            print "Sending message to: " + str(channel) + " : " + str(message)
            self.slack_client.api_call("chat.postMessage", channel=channel, text=message, as_user=True)
