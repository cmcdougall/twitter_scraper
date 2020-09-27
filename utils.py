import re
from datetime import datetime, timedelta
from pytz import reference

# Regexes to parse posted times in tweets
TIME_UNIT = r'(\d+)([s|m|h])'
CURRENT_YEAR = r'(\w+)\s+(\d+)'
PAST_YEAR = r'(\d+)\s+(\w+)\s+(\d+)'


def get_text_from_css_selector(el, selector_query: str) -> str:
    """
    Find a HTML element using CSS Selector
    :param el: The parent HTML element
    :param selector_query: A CSS Selector query used to find the child element
    :return: A text within the HTML element
    """
    text = None
    elements = el.select(selector_query)
    if len(elements) > 0:
        text = elements[0].get_text().strip()

    return text


def get_estimated_timestamp(posted_ago: str, current_time: datetime):
    """
    Returns an estimated unix timestamp and a display date in UTC for when the tweet was posted
    :param posted_ago: The display posted time from the tweet
    :param current_time: The current time to use to perform the estimation
    :return: A tuple of the unix timestamp, and the display date in UTC
    """
    match = re.match(TIME_UNIT, posted_ago)
    if match:
        duration = int(match.group(1))
        unit = match.group(2)

        if unit == 's':
            current_time -= timedelta(seconds=duration)
        elif unit == 'm':
            current_time -= timedelta(minutes=duration)
        elif unit == 'h':
            current_time -= timedelta(hours=duration)
    else:
        match = re.match(CURRENT_YEAR, posted_ago)
        if match:
            # Append the current year to the string, so the datetime object has the correct year
            posted_ago = f'{posted_ago} {current_time.year}'
            current_time = datetime.strptime(posted_ago, '%b %d %Y')
        else:
            match = re.match(PAST_YEAR, posted_ago)
            if match:
                current_time = datetime.strptime(posted_ago, '%d %b %y')

    # Convert to milliseconds before returning
    return int(current_time.timestamp() * 1000), current_time.strftime('%d %b %Y %H:%M %Z')
