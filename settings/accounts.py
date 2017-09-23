# -*- coding: utf-8 -*-
import json
import codecs
import os
path = os.path.abspath(".")

# please set this to your own, this is fake accounts

# user need to specify user.json file to store user ids the format would be
# [
#   {
#         "id": "a",
#         "password": "b"
#   },
#   {
#         "id": "c",
#         "password": "d"
#   }
# ]

with codecs.open(path + "/settings/user.json", "r", "utf8") as f:
    accounts = json.loads(f.read())

