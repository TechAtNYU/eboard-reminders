#
# Cole Smith
# Event Reminder for Tech@NYU
# EventGrabber.py
#

import requests

import Event


class EventGrabber(object):
    def __init__(self, url, auth_token):
        """
        :param url: string
        :param auth_token: string
        """
        self.url = url + '/events/upcoming?include=addedBy'
        self.auth_token = auth_token

    def get_list_of_upcoming_events(self):
        """
        Accesses Intranet API to get a JSON object of
        upcoming events
        :return: Array of Events
        """
        events = []
        auth = "Bearer " + self.auth_token
        req = requests.get(self.url, headers={"Authorization": auth})
        try:
            data = req.json()
            data_iteration = 0
            for key in data["data"]:
                att = key["attributes"]
                event = Event.Event(key["id"], "NO NAME", att["title"], att["startDateTime"],
                                    att["endDateTime"], att["status"])

                included_iteration = 0
                for keyi in data["included"]:
                    if included_iteration == data_iteration:
                        event.creator = keyi["attributes"]["name"]
                    included_iteration += 1

                event.event_url = key["links"]["self"]
                event.check_event_for_errors()
                events.append(event)
                data_iteration += 1

        except ValueError:
            print "[ ERR ] Error in grabbing events from Intranet"

        return events
