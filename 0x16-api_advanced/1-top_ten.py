#!/usr/bin/python3
"""return subscribers"""
import requests


def top_ten(subreddit):
    """return subscribers"""
    if not subreddit or not isinstance(subreddit, str):
        print(None)
        return
    r = requests.get(
        'https://www.reddit.com/r/{}/hot.json'.format(subreddit),
        headers={'User-Agent': "omar"})
    if r.status_code == 200:
        data = r.json()["data"]
        for i in range(10):
            print(data["children"][i]['data']['title'])
        return
    print(None)
