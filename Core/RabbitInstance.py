import pika
from pika import BlockingConnection
from pika.adapters.blocking_connection import BlockingChannel
from Core.BaseAlgObject import BaseAlgObject


class RabbitException(Exception):
    def __init__(self, line: str):
        BaseAlgObject.logger.error(f"Alg exception {line}")
        super().__init__(line)


class RabbitBase:
    base_queue_name = 'Test1'
    queue: dict = {}

    def __init__(self) -> None:
        self.connection: BlockingConnection = None
        self.channel: BlockingChannel = None

    def connect(self) -> None:
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            self.channel = self.connection.channel()
        except Exception as ex:
            raise RabbitException(f'connect exception: {ex}')

    def disconnect(self) -> None:
        try:
            self.connection.close()
            self.connection = None
            self.channel = None
        except Exception as ex:
            raise RabbitException(f'connect exception: {ex}')

    def add_queue(self, queue_name: str) -> None:
        if queue_name in RabbitBase.queue:
            BaseAlgObject.logger.warning(f"add_queue already have {queue_name}")
        try:
            rabbit_queue = self.channel.queue_declare(queue=queue_name)
        except Exception as ex:
            raise RabbitException(f'add_queue exception: {ex}')
        RabbitBase.queue[queue_name] = {'rabbit_queue': rabbit_queue, 'myself': self}

    def del_queue(self, queue_name: str) -> None:
        if queue_name in RabbitBase.queue:
            raise RabbitException(f'Queue {queue_name} already exist')
        queue = RabbitBase.queue[queue_name]
        self.channel.queue_delete(queue_name)
        del RabbitBase.queue[queue_name]


class RabbitPublishInstance(RabbitBase):
    def __init__(self) -> None:
        super().__init__()

    def publish(self, queue_name: str, body: bytes) -> None:
        try:
            self.channel.basic_publish(exchange='', routing_key=queue_name, body=body)
        except Exception as ex:
            raise RabbitException(f'publish exception: {ex}')


class RabbitSubscribeInstance(RabbitBase):
    def __init__(self) -> None:
        super().__init__()

    def consume_register(self, queue_name: str, auto_ack: bool = True) -> None:
        if queue_name not in RabbitBase.queue:
            raise RabbitException(f'Queue {queue_name} not exist')
        try:
            consumer_tag = self.channel.basic_consume(
                queue=queue_name, auto_ack=auto_ack, on_message_callback=self.callback_static)
            queue = RabbitBase.queue[queue_name]
            queue['consumer_tag'] = consumer_tag
        except Exception as ex:
            raise RabbitException(f'consume exception: {ex}')

    def consume_unregister(self, queue_name: str) -> None:
        if queue_name not in RabbitBase.queue:
            raise RabbitException(f'Queue {queue_name} not exist')
        try:
            queue = RabbitBase.queue[queue_name]
            self.channel.basic_cancel(queue['consumer_tag'])
        except Exception as ex:
            raise RabbitException(f'consume exception: {ex}')

    def start_consuming(self) -> None:
        # blocking call
        try:
            self.channel.start_consuming()
        except Exception as ex:
            raise RabbitException(f'start_cosuming exception: {ex}')

    def stop_consuming(self) -> None:
        try:
            self.channel.stop_consuming()
        except Exception as ex:
            raise RabbitException(f'stop_consuming exception: {ex}')

    @staticmethod
    def callback_static(channel: str, method: str, properties: str, body: bytes) -> None:
        queue = RabbitBase.queue[RabbitBase.base_queue_name]
        myself: RabbitSubscribeInstance = queue['myself']
        myself.callback(channel, method, properties, body)

    def callback(self, channel, method, properties, body) -> None:
        print(f'channel: {channel}, method: {method}, properties: {properties}, body: {body}')
