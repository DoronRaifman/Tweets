import os
import sys
import time

from Core.BaseAlgObject import BaseAlgObject
from Core.RabbitInstance import RabbitBase, RabbitSubscribeInstance


class TestRabbitSubscribe(RabbitSubscribeInstance):
    def __init__(self):
        super().__init__()

    def do_work(self):
        self.connect()
        self.add_queue(queue_name=self.base_queue_name)
        self.consume_register(queue_name=self.base_queue_name, auto_ack=True)
        self.start_consuming()

    def callback(self, channel, method, properties, body):
        # print(channel: {channel}, method: {method}, properties: {properties}, body: {body}')
        print(f'body: {body}')


if __name__ == '__main__':
    publisher = TestRabbitSubscribe()
    try:
        publisher.do_work()
    except KeyboardInterrupt:
        BaseAlgObject.logger.debug('Interrupted')
        publisher.stop_consuming()
        publisher.disconnect()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

