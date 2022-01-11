import threading

from Applications.Client import Client
from Applications.Server import Server
from Applications.TweetsReader import TweetsReader


class Application:
    def __init__(self) -> None:
        self.tweets: TweetsReader = TweetsReader()

    def prepare_for_clients(self) -> None:
        self.tweets.read_csv()

    def login(self, user_info: dict) -> None:
        server = Server(user_info)
        server.start_queue()
        server_thread = threading.Thread(target=server.publish_tweets_messages)
        server_thread.start()

        client = Client()
        client.login(user_info)
        client_thread = threading.Thread(target=client.read_tweets)
        client_thread.start()


if __name__ == '__main__':
    application = Application()
    application.prepare_for_clients()
    country, range = 'Israel', 85.0
    for city_name in Server.locations[country].keys():
        user_name = city_name
        user_info = {
            'user_name': user_name, 'loc_country': country, 'loc_city': city_name, 'range': range,
            'phrase': 'I have arrived'
        }
        application.login(user_info)
        break

