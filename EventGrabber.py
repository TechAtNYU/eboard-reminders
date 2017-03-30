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

                # Get values from attributes for Event init
                id = ""
                name = ""
                title = ""
                startDateTime = ""
                endDateTime = ""
                status = ""
                url = ""

                att = key["attributes"]

                if "id" in key:
                    id = key["id"]
                if "title" in att:
                    title = att["title"]
                if "startDateTime" in att:
                    startDateTime = att["startDateTime"]
                if "endDateTime" in att:
                    endDateTime = att["endDateTime"]
                if "status" in att:
                    status = att["status"]
                if "self" in key["links"]:
                    url = key["links"]["self"]

                # Find Name
                included_iteration = 0
                for incl in data["included"]:
                    if included_iteration == data_iteration:
                        name = incl["attributes"]["name"]
                    included_iteration += 1

                # Create and check event
                event = Event.Event(id, name, title, startDateTime, endDateTime, status)
                event.event_url = url
                event.check_event_for_errors()
                events.append(event)
                data_iteration += 1

        except ValueError:
            print "[ ERR ] Error in grabbing events from Intranet"

        return events
