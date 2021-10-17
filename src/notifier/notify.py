"""Notifier class """
import logging
import requests

class Notify(object):
    """Notified objects are populating in that class"""
    def __init__(self):
        self._webhook_url = None


    def prepare_message(self, message, metric):
        """ Prepare the slack messages according to the slack API compability """
        body = {
        'text': "EKS Cluster Audit Logs",
        'attachments': [{
        'text': "CIS",
        'fields': [
            {
                'title': 'Event Message',
                'value': message,
                'short': True
            },
            {
                'title': 'The observed event count related query',
                'value': metric,
                'short': True
            }
            ]
        }],
        }

        return body

    @property
    def webhook_url(self):
        """ Getter function sender """
        if len(self._webhook_url) != 0:
            logging.info("Webhook Url set!")
        else:
            logging.error("There is no webhook url")

    @webhook_url.setter
    def webhook_url(self, value):
        self._webhook_url = value


    def send_message(self, content, metric_key):
        """ Message sender """

        message_body = self.prepare_message(message=content, metric=metric_key)
        webhook_url = self._webhook_url
        try:
            notification_status = requests.post(webhook_url, json=message_body)
            
            notification_status.raise_for_status()

        except requests.exceptions.HTTPError as error:
            logging.error("HTTP error {}".format(error))
        except requests.exceptions.ConnectionError as error:
            logging.error("ConnectionError error {}".format(error))
        except requests.exceptions.Timeout as error:
            logging.error("Timeout error {}".format(error))
        except requests.exceptions.RequestException as error:
            logging.error("RequestException error {}".format(error))
