import math
import time
from Core.RabbitInstance import RabbitPublishInstance
from Applications.TweetsReader import TweetsReader


class Server:
    tweets = TweetsReader()
    locations = {
        'Israel': {
            'Jerusalem': {'x': 80.0, 'y': 100.0},
            'Tel Aviv': {'x': 10.0, 'y': 100.0},
            'Haifa': {'x': 10.0, 'y': 200.0},
            'Ashqelon': {'x': 10.0, 'y': 50.0},
            'Taberias': {'x': 80.0, 'y': 200.0},
            'BeerSheva': {'x': 70.0, 'y': 10.0},
        }
    }

    def __init__(self, user_info: dict) -> None:
        self.user_info = user_info
        self.rabbit = RabbitPublishInstance()
        self.queue_name = ''

    @classmethod
    def read_tweets(cls):
        cls.tweets.read_csv()

    def start_queue(self) -> None:
        self.queue_name = self.user_info['user_name']
        self.rabbit.connect()
        self.rabbit.add_queue(queue_name=self.queue_name)

    def get_location(self, loc_country: str, loc_city: str) -> (float, float):
        loc_cities = self.locations[loc_country]
        location = loc_cities[loc_city]
        x, y = location['x'], location['y']
        return x, y

    def publish_tweets_messages(self) -> None:
        time.sleep(1)
        for index, tweet in enumerate(self.tweets.tweets):
            user_x, user_y = self.get_location(self.user_info['loc_country'], self.user_info['loc_city'])
            msg_country = tweet[self.tweets.field_indexs['loc_country']]
            msg_city = tweet[self.tweets.field_indexs['loc_city']]
            msg_x, msg_y = self.get_location(msg_country, msg_city)
            distance = round(math.sqrt(pow(msg_x-user_x, 2.0) + pow(msg_y-user_y, 2.0)), 0)
            max_distance = self.user_info['range']
            if distance > max_distance:
                # print(f'distance not ok {distance} > {max_distance}')
                continue
            # else:
            #   print(f'distance ok {distance} <= {max_distance}')
            user_name = self.user_info['user_name']
            message_dict = {field_name: tweet[field_ndx] for field_name, field_ndx in self.tweets.field_indexs.items()}
            message_dict['user_name']: user_name
            user_phrase, msg_phrase = self.user_info['phrase'], message_dict['phrase']
            if user_phrase not in msg_phrase:
                # print(f'phrase: user "{user_phrase}" not in "{msg_phrase}"')
                continue
            message = bytes(f'Message {index}, {str(message_dict)}', 'utf-8')
            print(f'publish user: {user_name}, msg: {message}')
            self.rabbit.publish(queue_name=user_name, body=message)
            time.sleep(0.1)
        self.rabbit.disconnect()

