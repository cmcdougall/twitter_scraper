import threading
import requests
from bs4 import BeautifulSoup
from tweet import Tweet
from urllib import parse
import time

URL = 'https://mobile.twitter.com/'
USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13F69 Twitter for iPhone'


class Scraper(threading.Thread):

    def __init__(self, account, tweets):
        threading.Thread.__init__(self)
        self.tweets = tweets
        self.printed_tweets = []
        self.scraped_tweets = set()
        self.first_print = True

        # Starting a session to automatically handle Cookie headers
        self.s = requests.session()

        # If the user has entered a username starting with '@', remove it
        self.account = account
        if self.account.startswith('@'):
            self.account = self.account[1:]

    def start_twitter_session(self):
        # Using a common iPhone User Agent
        headers = {
            'User-Agent': USER_AGENT
        }

        # Accessing the Javascript-less Twitter site. Using a proxy I found that the initial request redirects you to the same URL, but with cookies set it asks if you
        self.s.get(f'{URL}{parse.quote(self.account)}', headers=headers)

    def scrape_tweets(self):
        # I found using a proxy these were the headers the server was expecting
        headers = {
            'Host': 'mobile.twitter.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': f'{URL}{parse.quote(self.account)}',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'
        }
        r = self.s.post(f'{URL}i/nojs_router?path=%2F{parse.quote(self.account)}',
                        headers=headers)
        bs = BeautifulSoup(r.text, 'html.parser')

        for tweet_table in bs.select('table.tweet'):
            new_tweet = Tweet.parse_tweet_table(tweet_table)
            if new_tweet is not None:
                if new_tweet.tweet_id not in self.scraped_tweets:
                    self.scraped_tweets.add(new_tweet.tweet_id)
                    self.tweets.append(new_tweet)
                    self.tweets.sort(key=lambda x: x.est_ts)

    def print_tweets(self):
        """
        Prints the most recent tweets. Only the most recent five tweets will be printed initially.
        :return:
        """

        if self.first_print:
            for tweet in self.tweets[-5:]:
                print(tweet, flush=True)

            # Record all tweet IDs so they aren't reprinted next loop
            [self.printed_tweets.append(tweet.tweet_id) for tweet in self.tweets]
            self.first_print = False
        else:
            for tweet in self.tweets:
                if tweet.tweet_id not in self.printed_tweets:
                    print(tweet, flush=True)
                    self.printed_tweets.append(tweet.tweet_id)

    def run(self):
        """
        Will scrape tweets then prints them out indefinitely. Sleeps for 10 minutes each loop
        :return:
        """
        self.start_twitter_session()

        while True:
            self.scrape_tweets()
            self.print_tweets()

            time.sleep(600)
