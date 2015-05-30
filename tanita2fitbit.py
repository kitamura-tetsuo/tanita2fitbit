#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This was taken, and modified from python-oauth2/example/client.py,
License reproduced below.

--------------------------
The MIT License

Copyright (c) 2007 Leah Culver

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

Example consumer. This is not recommended for production.
Instead, you'll want to create your own subclass of OAuthClient
or find one that works with your web framework.
"""



import requests
import json
import datetime
import configparser
import webbrowser


DEFAULT_CONFIG_FILE = "tanita2fitbit.cfg"

config = configparser.SafeConfigParser()
config.read(DEFAULT_CONFIG_FILE)

token = {}

try:
    from urllib.parse import urlencode
except ImportError:
    # Python 2.x
    from urllib import urlencode

from requests_oauthlib import OAuth1, OAuth1Session

import time, random, urllib, cgi, hmac, hashlib


token["refresh_token"] = config.get("tanita","refresh_token")
token["expires_in"] = config.get("tanita","expires_in")
token["access_token"] = config.get("tanita","access_token")

if token["access_token"] == "":
    consumer_key = "99.xcVA8AAg6H.apps.healthplanet.jp"                             # Consumer Key
    consumer_secret = "1431352267466-EM9IerRgOao11LmtlmEp5NyL0PwOKYRD9EDTMf4X"         # Consumer Secret

    # Request Token は GET で取得
    method = "GET"

    # Request Token 取得の URL
    request_token_url = "https://www.healthplanet.jp/oauth/auth"
    url = "https://www.healthplanet.jp/oauth/auth?client_id=99.xcVA8AAg6H.apps.healthplanet.jp&redirect_uri=https://www.healthplanet.jp/success.html&scope=innerscan&response_type=code"

    webbrowser.open(url)

    AUTH_CODE = ""

    try:
        AUTH_CODE = raw_input("ブラウザに表示された Codeを入力してください: ")
    except NameError:
        # Python 3.x
        AUTH_CODE = input("ブラウザに表示された Codeを入力してください: ")


    REDIRECT_URI = "https://www.healthplanet.jp/success.html"

    #session = requests.Session()

    data = {
    	"client_id": consumer_key,
    	"client_secret": consumer_secret,
    	"redirect_uri": REDIRECT_URI,
    	"code": AUTH_CODE,
    	"grant_type": "authorization_code"
    }

    response = requests.post("https://www.healthplanet.jp/oauth/token", data=data)

    print(response)
    status_list = response.json()
    print(status_list)

    for status in status_list:
        print(status)
    token["refresh_token"] = status_list["refresh_token"]
    token["expires_in"] = status_list["expires_in"]
    token["access_token"] = status_list["access_token"]
    config.set("tanita", "refresh_token", token["refresh_token"])
    config.set("tanita", "expires_in", str(token["expires_in"]))
    config.set("tanita", "access_token", token["access_token"])
    config.write(open(DEFAULT_CONFIG_FILE, "w"))

response = requests.get("https://www.healthplanet.jp/status/innerscan.json?access_token={0}&date=1".format(token["access_token"]))

print(response)

status_list = response.json()
print(status_list)

for status in status_list:
    print(status)
    print(status_list[status])
    

data_list = status_list["data"]

import re

for data in data_list:
    print(data)
    for param_name in data:
        print(param_name)
        if param_name == "date":
            print(data[param_name])





import os
import pprint
import sys

import fitbit


CLIENT_KEY = "049ca8fcbabafb04d070b67c3f29570c"
CLIENT_SECRET = "d56183c787edbd4df4e0f7ec2df9f269"

token["oauth_token"] = config.get("fitbit","oauth_token")
token["oauth_token_secret"] = config.get("fitbit","oauth_token_secret")
token["encoded_user_id"] = config.get("fitbit","encoded_user_id")

pp = pprint.PrettyPrinter(indent=4)
if token["oauth_token"] == "":
    print("** OAuth Python Library Example **\n")
    client = fitbit.FitbitOauthClient(CLIENT_KEY, CLIENT_SECRET)

    # get request token
    print("* Obtain a request token ...\n")
    token = client.fetch_request_token()
    print("RESPONSE")
    pp.pprint(token)
    print("")

    print("* Authorize the request token in your browser\n")
    stderr = os.dup(2)
    os.close(2)
    os.open(os.devnull, os.O_RDWR)
    webbrowser.open(client.authorize_token_url())
    os.dup2(stderr, 2)
    try:
        verifier = raw_input("Verifier: ")
    except NameError:
        # Python 3.x
        verifier = input("Verifier: ")

    # get access token
    print("\n* Obtain an access token ...\n")
    token = client.fetch_access_token(verifier)
    print("RESPONSE")
    pp.pprint(token)
    print("")
    config.set("fitbit", "oauth_token", token["oauth_token"])
    config.set("fitbit", "oauth_token_secret", token["oauth_token_secret"])
    config.set("fitbit", "encoded_user_id", token["encoded_user_id"])
    config.write(open(DEFAULT_CONFIG_FILE, "w"))

fitbitClient = fitbit.Fitbit(CLIENT_KEY, CLIENT_SECRET, resource_owner_key=token["oauth_token"], resource_owner_secret=token["oauth_token_secret"], user_id=token["encoded_user_id"], system="ja-JP" )

p = re.compile(r"(\d\d\d\d)(\d\d)(\d\d)(\d\d)(\d\d)")

for data in data_list:
    print(data)
    for param_name in data:
        print(param_name)
        date = re.sub(p, r"\1-\2-\3", data["date"])
        time = re.sub(p, r"\4:\5:00", data["date"])
        if data["tag"] == "6021":
            fitbitClient.log_body_weight(date=date, time=time, weight=data["keydata"])
        if data["tag"] == "6022":
            fitbitClient.log_body_fat(date=date, time=time, fat=data["keydata"])
        if data["tag"] == "6023":
            fitbitClient.body(date=date, data={"chest": data["keydata"]})




"""
tag
取得する測定部位を指定する。未指定の場合はデフォルトの値を取得する。カンマ区切りで指定する
6021 : 体重 (kg)
6022 : 体脂肪率 (%)
6023 : 筋肉量 (kg)
6024 : 筋肉スコア
6025 : 内臓脂肪レベル2(小数点有り、手入力含まず)
6026 : 内臓脂肪レベル(小数点無し、手入力含む)
6027 : 基礎代謝量 (kcal)
6028 : 体内年齢 (才)
6029 : 推定骨量 (kg)

"""
