import logging

import requests

from django.conf import settings

logger = logging.getLogger()

FROM='root@tilde.town'

def send_email(to, body, subject='a message from tilde.town', frum=FROM,):
    """Sends an email using mailgun. Logs on failure."""
    response =  requests.post(
        settings.MAILGUN_URL,
        auth=('api', settings.MAILGUN_KEY),
        data={
            'from': frum,
            'to': to,
            'subject': subject,
            'text': body
        }
    )

    if response.status_code != 200:
        logger.error('{}: failed to send email "{}" to {}'.format(
            response.status_code,
            subject,
            to))
