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
import codecs
from lxml import etree
#
# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")


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
        self.owner = None
        self.user_id = user_id
        self.filter = filter
        self.total_weibo_count = 0
        self.following = 0
        self.follower = 0
        self.contents = []
        self.soup = None
        self.__html = None

    def get_username(self):
        url = "http://weibo.com/u/%d"%(self.user_id)
        response = requests.get(url, cookies=self.cookie)
        if response.status_code == requests.codes.ok:
            selector = etree.HTML(response.content)
            selector_content = selector.xpath("//title/text()")
            if len(selector_content):
                self.owner = selector_content[0]
            if self.owner:
                print("Weibo owner: ", self.owner.encode("utf8"))
        else:
            print "Failed on getting owner name..."

    def get_user_info(self):
        url = "http://weibo.cn/u/%d?filter=%d&page=1"%(self.user_id,self.filter)
        response = requests.get(url, cookies=self.cookie)
        if response.status_code == requests.codes.ok:
            selector = etree.HTML(response.content)

            # find total weibo count
            pattern = r"\d+\.?\d*"
            weibo_count = selector.xpath("//div[@class='tip2']/span[@class='tc']/text()")
            #print  string_wb
            if len(weibo_count):
                self.total_weibo_count = filter(lambda x: x.isdigit(), weibo_count[0])
                print "Total Weibo: ", self.total_weibo_count
            else:
                print("Getting weibo count failed.")

            # find following count
            following = selector.xpath("//div[@class='tip2']/a/text()")
            if len(following):
                self.following = filter(lambda x: x.isdigit(), following[0])
                print "Total following: ", self.following
            else:
                print("Getting following failed")

            # get follower
            follower = selector.xpath("//div[@class='tip2']/a/text()")
            if len(follower) > 1:
                self.follower = filter(lambda x: x.isdigit(), follower[1])
                print("Total follower: ", self.follower)
            else:
                print("Getting follower failed")

    def get_weibo_contents(self):
        url = "http://weibo.cn/u/%d?filter=%d&page=1"%(self.user_id,self.filter)
        html = requests.get(url, cookies = self.cookie).content
        selector = etree.HTML(html)
        if selector.xpath('//input[@name="mp"]')==[]:
            page_number = 1
        else:
            page_number = (int)(selector.xpath('//input[@name="mp"]')[0].attrib['value'])

        original_count = 0
        for page in range(1, page_number + 1):
            url2 = 'http://weibo.cn/u/%d?filter=%d&page=%d'%(self.user_id,self.filter,page)
            html2 = requests.get(url2, cookies = self.cookie).content
            selector2 = etree.HTML(html2)
            info = selector2.xpath("//div[@class='c']")
            if len(info) > 3:
                for i in range(0, len(info) - 2):
                    original_count += 1
                    # actual content
                    text = info[i].xpath("div/span[@class='ctt']")
                    try:
                        print text[0].xpath('string(.)').encode("utf8")
                    except Exception as e:
                        continue

                    # total like
                    like = info[i].xpath("div/a/text()")[-4]
                    print "like: ", filter(lambda x: x.isdigit(), like)

                    # forward
                    forward = info[i].xpath("div/a/text()")[-3]
                    print "forward: ", filter(lambda x: x.isdigit(), forward)

                    # total comments
                    comments = info[i].xpath("div/a/text()")[-2]
                    print "comments: ", filter(lambda x: x.isdigit(), comments)

def main():
    with open("user.json", "r") as f:
        data = json.loads(f.read())
    username = data["username"]
    password = data["password"]
    cookies = get_cookies.login(username=username, password=password)
    weibo = Weibo(user_id=1669879400, cookie=cookies)
    weibo.get_username()
    weibo.get_user_info()
    weibo.get_weibo_contents()


if __name__ == "__main__":
    main()