from Core.RabbitInstance import RabbitSubscribeInstance


class Client(RabbitSubscribeInstance):
    def __init__(self):
        super().__init__()
        self.user_info = {}

    def login(self, user_info: dict) -> None:
        self.user_info = user_info

    def read_tweets(self) -> None:
        self.connect()
        queue_name = self.user_info['user_name']
        self.add_queue(queue_name=queue_name)
        self.consume_register(queue_name=queue_name)
        self.start_consuming()

    def callback(self, channel: str, method: str, properties: str, body: bytes) -> None:
        # print(channel: {channel}, method: {method}, properties: {properties}, body: {body}')
        print(f'rx callback. user: {self.user_info["user_name"]}, body: {body}')
