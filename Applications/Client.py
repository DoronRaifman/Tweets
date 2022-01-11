from Core.RabbitInstance import RabbitSubscribeInstance


class Client(RabbitSubscribeInstance):
    def __init__(self):
        super().__init__()
        self.user_name, self.loc_country, self.loc_city, self.range = None, None, None, 40.0

    def login(self, user_name: str, loc_country: str, loc_city: str, range: float) -> None:
        self.user_name, self.loc_country, self.loc_city, self.range = user_name, loc_country, loc_city, range

    def read_tweets(self) -> None:
        self.connect()
        self.add_queue(queue_name=self.user_name)
        self.consume_register(queue_name=self.user_name)
        self.start_consuming()

    def callback(self, channel: str, method: str, properties: str, body: bytes) -> None:
        # print(channel: {channel}, method: {method}, properties: {properties}, body: {body}')
        print(f'user: {self.user_name}, body: {body}')
