from threading import Thread
import app.data_gathering as data

reddit_cred = {
    'app_id': '',
    'secret': '',
    'username': '',
    'password': '',
    'user_agent': ''
}

twitter_cred = {
    'consumer_key': '',
    'consumer_secret': '',
    'access_token_key': '',
    'access_token_secret': ''
}

reddit = data.Reddit(client_id=reddit_cred.get('app_id'),
                     client_secret=reddit_cred.get('secret'),
                     username=reddit_cred.get('username'),
                     password=reddit_cred.get('password'),
                     user_agent=reddit_cred.get('user_agent'))

twitter = data.Twitter(con_key=twitter_cred.get("consumer_key"),
                       con_secret=twitter_cred.get("consumer_secret"),
                       access_key=twitter_cred.get("access_token_key"),
                       access_secret=twitter_cred.get("access_token_secret"))


def main():
    t1 = Thread(target=reddit.stream, args=['investing+cryptocurrency+securityanalysis+wallstreetbets'])
    t2 = Thread(target=twitter.stream, args=[['ASX', 'australian stock exchange', 'NYSE', 'new york stock exchange', ], ['en']])
    t1.start()
    t2.start()


if __name__ == '__main__':
    main()
