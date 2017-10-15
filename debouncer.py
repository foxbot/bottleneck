""" This module contains the debouncer """

from collections import deque
from time import sleep
from threading import Thread
from discord import Webhook, RequestsWebhookAdapter

class Debouncer(Thread):
    """ A debouncer for webhooks """

    def __init__(self, config):
        Thread.__init__(self)

        self.queue = deque([])
        self.config = config

        self.delay = config['delay'] or 5
        self.batch_size = config['batch_size'] or 10

        self.webhook = Webhook.from_url(self.config['url'], adapter=RequestsWebhookAdapter())

    def push(self, data):
        """ Append a webhook to discord """
        self.queue.append(data)

    def send(self):
        """ Send the webhooks in the queue to discord """
        items = []
        for _ in range(self.batch_size):
            if not self.queue:
                break

            item = self.queue.popleft()
            items.append(item)

        self.webhook.send(embeds=items)

    def run(self):
        while True:
            while self.queue:
                self.send()
            sleep(self.delay)