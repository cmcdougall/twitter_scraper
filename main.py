from flask import Flask, jsonify
import argparse
from scraper import Scraper
import logging

# Disable Flask logging, unless it's an error
LOG = logging.getLogger('werkzeug')
LOG.setLevel(logging.ERROR)

app = Flask(__name__)
TWEETS = []


@app.route('/export')
def export():
    """
    Returns a list of tweets in JSON format
    :return: List of tweets
    """
    return jsonify([tweet.get_json() for tweet in TWEETS])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrapes a twitter account')
    parser.add_argument('--account', help='The Twitter account to scrape', required=True)
    args = parser.parse_args()

    # Start the scraper on a different thread
    scraper = Scraper(args.account, TWEETS)
    scraper.start()

    # Start the Flask server
    app.run(host='0.0.0.0', debug=False, use_reloader=False)
