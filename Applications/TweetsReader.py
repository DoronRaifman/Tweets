import os


class TweetsReader:
    csv_file_name = os.path.abspath(os.path.join('..', 'Data', 'TweeterData.csv'))
    tweets = []
    field_names = []
    field_indexs = {}

    def __init__(self):
        pass

    @classmethod
    def read_csv(cls) -> list:
        with open(cls.csv_file_name, 'rt') as file_descriptor:
            lines = file_descriptor.readlines()
            if len(lines) > 0:
                cls.field_names = lines[0][:-1].split(',')
                cls.field_indexs = {field_name: index for index, field_name in enumerate(cls.field_names)}
            if len(lines) > 1:
                for line in lines[1:][:-1]:
                    if len(line) > 10:
                        fields_values = line.split(',')
                        cls.tweets.append(fields_values)
                    else:
                        break
        return cls.tweets


if __name__ == '__main__':
    tweets = TweetsReader().read_csv()
    print(f'read tweets: we have {len(tweets)} tweets')
