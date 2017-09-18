# -*- coding: utf-8 -*-
import re
import string
import os
import urllib
import urllib2
from bs4 import BeautifulSoup
import requests
import json
import traceback
import pdb

# user defined packages
import get_cookies

class Content(object):
    def __init__(self, text, like_count, forward_count, comment_count, comments=None):
        self.text = text
        self.like_count = like_count
        self.forward_count = forward_count
        self.comment_count = comment_count

        # comments should be a list of text here we set it as none for now
        self.comments = comments

class Weibo(object):
    def __init__(self, user_id, filter=0, cookie=None):
        # setting cookie is superrrr important!!! otherwise cannot connect
        self.cookie = cookie
        self.user_id = user_id
        self.filter = filter
        self.total_weibo_count = 0
        self.following = 0
        self.follower = 0
        self.contents = []
    def get_username(self):
        url = "http://weibo.com/u/%d"%(self.user_id)
        html = requests.get(url, cookies=self.cookie).content
        print html




def main():
    with open("user.json", "r") as f:
        data = json.loads(f.read())
    username = data["username"]
    password = data["password"]
    cookies = get_cookies.login(username=username, password=password)
    weibo = Weibo(user_id=1669879400, cookie=cookies)
    weibo.get_username()


if __name__ == "__main__":
    main()