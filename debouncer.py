""" This module contains the debouncer """

import sys
from time import sleep
from threading import Thread
from discord import Webhook, RequestsWebhookAdapter
from raven import Client

class Debouncer(Thread):
    """ A debouncer for webhooks """

    def __init__(self, config):
        Thread.__init__(self)
        self.daemon = True

        self.queue = []
        self.config = config

        self.delay = config['delay']
        self.batch_size = config['batch_size']

        self.webhook = Webhook.from_url(config['url'], adapter=RequestsWebhookAdapter())
        if config['sentry']:
            self.raven = Client(config['sentry'])

    def push(self, data):
        """ Append a webhook to discord """
        self.queue.append(data)

    def send(self):
        """ Send the webhooks in the queue to discord """
        items = []
        for _ in range(self.batch_size):
            if not self.queue:
                break

            item = self.queue.pop(0)
            items.append(item)

        self.webhook.send(embeds=items)

    def run(self):
        try:
            self._run()
            print("Thread ran to completion?", file=sys.stderr)
            sys.exit(1)
        except:
            if self.raven:
                self.raven.captureException()
            # Kill the process so supervisord can restart
            sys.exit(1)

    def _run(self):
        while True:
            while self.queue:
                self.send()
            sleep(self.delay)
