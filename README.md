# Twitter Scraper

Scrapes a Twitter account every 10 minutes. The project has been designed to run locally and through a Docker container.

I am using the development Flask server, was unsure if it was supposed to be run in a WSGI.

# Running locally

Have Python 3.8 installed. Create a virtual environment, and install dependencies:

```python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

The execute the following to start the scraper and a Flask server to export all collected tweets:

```python
python main.py --account <twitter account to scrape>
```

# Running in a Docker Container

Build the Docker image:

```
docker build . -t twitter_scraper
```

Run the Docker Image by executing the following:

```
docker run -p 5000:5000 twitter_scraper python -u main.py --account swiftonsecurity
```

Usage details will be displayed if the python command or the account argument is omitted.

# REST API

The API is exposed on port 5000.

## /export

Returns a list of all collected tweets since the scraper started. The JSON returned:

```
[
    {
        'username': str,                # User that posted the tweet
        'displayName': str,             # The user's display name
        'tweetId': int,                 # Tweet ID
        'estimatedPostTimestamp': int,  # The estimated time it was posted based on the collectedTimestamp, and the postedAgo value in epoch milliseconds
        'text': str,                    # Tweet contents
        'collectedTimestamp': int,      # The time is was scraped in epoch milliseconds
        'postedAgo': str,               # The Twitter website displays how long ago it was posted. This value is used to estimate when it was posted.
        'context': str                  # The context the tweet was made, usually specifies if it was a retweet
    }
    ...
]
```

### curl example

```
curl localhost:5000/export
```

# Known Issues

While testing I discovered that if a user deletes a tweet within the 10 minute window, an old tweet will be printed out.

Was thinking of displaying tweets after a certain time, but decided not to.
