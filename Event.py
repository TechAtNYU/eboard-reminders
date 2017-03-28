#
# Cole Smith
# Event Reminder for Tech@NYU
# Event.py
#

import datetime


class Event(object):
    def __init__(self, event_id, creator, title, time_start, time_end, status):
        """
        Defines an event from the Intranet
        :param creator: string
        :param title: string
        :param time_start: string
        :param time_end: string
        :param status: string
        """
        self.event_id = event_id
        self.creator = creator
        self.title = title
        self.start_time = Event.format_time_object(time_start)
        self.end_time = Event.format_time_object(time_end)
        self.status = status
        self.event_url = ""
        self.errors = []

    @staticmethod
    def format_time_object(time_string):
        """
        Takes time string from HTTP request and formats it to datetime object
        :param time_string: a string in the form 2019-01-01T05:00:00.000Z
        :return: datetime object of specified time
        """
        time_string = time_string.split('-')
        time_string = time_string[:2] + time_string[2].split('T')
        time_string = time_string[:3] + time_string[3].split(':')[:2]

        # Time parts: [year month day hour minute]

        year = int(time_string[0])
        month = int(time_string[1])
        day = int(time_string[2])
        hour = int(time_string[3])
        minute = int(time_string[4])

        return datetime.datetime(year, month, day, hour, minute)

    # Method to check event for errors
    def check_event_for_errors(self):
        """
        Checks event for given abnormalities
        :return: Array of errors as strings
        """
        # Define abnormal event length
        LENGTH_ERROR = datetime.timedelta(hours=2)
        # Define abnormal event hours
        START_TIME_ERROR_1 = datetime.time(hour=14)
        START_TIME_ERROR_2 = datetime.time(hour=20)

        if self.start_time.hour < START_TIME_ERROR_1.hour:
            self.errors.append("Alert: Event starts before 2 PM")
        elif self.start_time.hour > START_TIME_ERROR_2.hour:
            self.errors.append("Alert: Event starts after 10PM")

        if self.end_time - self.start_time > LENGTH_ERROR:
            self.errors.append("Alert: Event longer than two hours")

        if not self.status == "announced":
            self.errors.append("Alert: Event is not marked as announced (Marked as " + self.status + ")")
