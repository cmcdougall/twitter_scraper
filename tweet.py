from typing import Mapping
from utils import get_text_from_css_selector, get_estimated_timestamp
from datetime import datetime
import pytz


class Tweet:

    def __init__(self, username: str, display_name: str, tweet_id: int, collected_ts: int, posted_ago_display_text: str,
                 est_ts: int, display_time: str, text: str, context: str = '') -> None:
        self.username = username
        self.display_name = display_name
        self.tweet_id = tweet_id
        self.est_ts = est_ts
        self.display_time = display_time
        self.text = text
        self.collected_ts = collected_ts
        self.posted_ago_display_text = posted_ago_display_text
        self.context = context if context is not None else ''

    def get_json(self) -> Mapping:
        """
        :return: Dictionary representation of a tweet
        """
        return {
            'username': self.username,
            'displayName': self.display_name,
            'tweetId': self.tweet_id,
            'estimatedPostTimestamp': self.est_ts,
            'text': self.text,
            'collectedTimestamp': self.collected_ts,
            'postedAgo': self.posted_ago_display_text,
            'context': self.context
        }

    def __str__(self):
        return f"{self.display_time} (estimated), {self.display_name} ({self.username}): {self.text}"

    @staticmethod
    def parse_tweet_table(tweet_table_element):
        """
        Parses a HTML table element into a tweet object
        :param tweet_table_element: The HTML table element
        :return: Tweet object or None if the table could not be parsed
        """
        current_datetime = datetime.now(tz=pytz.utc)
        collected_ts = int(current_datetime.timestamp() * 1000)

        username = get_text_from_css_selector(tweet_table_element, 'a > div.username')
        display_name = get_text_from_css_selector(tweet_table_element, 'a > strong.fullname')
        text = get_text_from_css_selector(tweet_table_element, 'div.tweet-text')
        context = get_text_from_css_selector(tweet_table_element, '.tweet-social-context > .context')

        tweet_id = None
        tweet_id_el = tweet_table_element.find(attrs={'data-id': True})
        if tweet_id_el is not None:
            tweet_id = tweet_id_el.get('data-id')

        posted_text = get_text_from_css_selector(tweet_table_element, 'td.timestamp')
        est_ts, display_time = get_estimated_timestamp(posted_text, current_datetime)

        if username is not None and display_name is not None and text is not None and tweet_id is not None:
            return Tweet(username=username, display_name=display_name, tweet_id=tweet_id, est_ts=est_ts,
                         display_time=display_time, text=text, collected_ts=collected_ts,
                         posted_ago_display_text=posted_text, context=context)
        else:
            return None
