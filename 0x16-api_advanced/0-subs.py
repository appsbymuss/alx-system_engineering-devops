#!/usr/bin/python3
"""return subscribers"""
import requests


def number_of_subscribers(subreddit):
    """return subscribers"""
    if not subreddit or not isinstance(subreddit, str):
        return 0
    r = requests.get(
        'https://www.reddit.com/r/{}/about.json'.format(subreddit),
        headers={'User-Agent': "mustapha"})
    if r.status_code == 200:
        data = r.json()["data"]
        return data["subscribers"]
    return 0
