import time
from Core.RabbitInstance import RabbitPublishInstance


class TestRabbitPublisher:
    def __init__(self):
        self.rabbit = RabbitPublishInstance()

    def do_work(self):
        self.rabbit.connect()
        self.rabbit.add_queue(queue_name=self.rabbit.base_queue_name)
        time.sleep(10)
        for i in range(10):
            time.sleep(0.1)
            message = bytes(f'Message {i}', 'utf-8')
            print(f'publish msg: {message}')
            self.rabbit.publish(queue_name=self.rabbit.base_queue_name, body=message)
        self.rabbit.disconnect()


if __name__ == '__main__':
    publisher = TestRabbitPublisher()
    publisher.do_work()


