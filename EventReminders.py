#
# Cole Smith
# Event Reminder for Tech@NYU
# EventReminders.py
#

import os
import datetime
import EventGrabber
import SlackInterpreter

# TODO: Check for events that happened two days ago


def update_queue(notification_queue, days):
    """
    Appends found events to notification_queue
    :param notification_queue: An Array of Events
    :param days: The days prior to event in which to remind the user
    :return: notification_queue
    """
    event_grabber = EventGrabber.EventGrabber(str(os.environ["INTRANET_URL"]), str(os.environ["INTRANET_TOKEN"]))
    upcoming_events = event_grabber.get_list_of_upcoming_events()

    for e in upcoming_events:
        time_from_today = datetime.date.today() + datetime.timedelta(days=days)
        if e.start_time.date() == time_from_today:
            print str(datetime.date.today()) + " : Event found for " + str(e.start_time.date()) + " : " + e.title
            notification_queue.append(e)

    return notification_queue


def notify_users(notification_queue):
    """
    Sends Notifications to users from the notification_queue
    :param notification_queue: An array of Events
    :return: None
    """
    for n in notification_queue:
        name_parts = n.creator.split()
        user = slack_interpreter.find_user_by_full_name(name_parts[0], name_parts[1])
        message = "Hello! This is a reminder that you have an event coming up, " + \
            n.title + " on " + str(n.start_time)

        slack_interpreter.send_message_to_user(user, message)

        if n.errors:
            errors = ""
            for e in n.errors:
                errors += e + "   "
        else:
            errors = "No errors found with event"

            slack_interpreter.send_message_to_user(user, errors)


if __name__ == '__main__':

    slack_interpreter = SlackInterpreter.SlackInterpreter()
    slack_interpreter.connect()

    queue = []
    queue = update_queue(queue, 7)
    queue = update_queue(queue, 2)
    notify_users(queue)
