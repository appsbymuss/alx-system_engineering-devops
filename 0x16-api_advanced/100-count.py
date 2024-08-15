#!/usr/bin/python3
"""return subscribers"""
import requests
from collections import OrderedDict

hot_title = []


def recurse(subreddit, hot_list=[]):
    """return subscribers"""
    if not subreddit or not isinstance(subreddit, str):
        return None
    if hot_list == []:
        r = requests.get(
            'https://www.reddit.com/r/{}/hot.json'.format(subreddit),
            headers={'User-Agent': "omar"})
        if r.status_code == 200:
            data = r.json()["data"]
        else:
            return None
        hot_list = data["children"]
    hot_title.append(hot_list[0]["data"]["title"])
    if hot_list[1:] == []:
        return hot_title
    return recurse(subreddit, hot_list[1:].copy())


def count_words(subreddit, word_list):
    """return subscribers"""
    title_list = recurse(subreddit)
    obj = {}
    for w in word_list:
        obj[w] = 0
        for t in title_list:
            obj[w] += (len(t.split(w)) - 1)
    for k, v in obj.items():
        if v:
            print("{}: {}".format(k, v))
