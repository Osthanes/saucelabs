#!/usr/bin/python

import requests
import sys
import json
import time
import os
import base64

SAUCE_URL = "https://saucelabs.com/rest/v1/"
SAUCE_USER = os.environ.get('SAUCE_USERNAME')
SAUCE_ACCESS_KEY = os.environ.get('SAUCE_ACCESS_KEY')
START_TIME = os.environ.get('EPOCH_TIME')

def request(url)
    base64 = base64.encodestring('%s:%s' % (SAUCE_USER, SAUCE_ACCESS_KEY).replace('\n', '')
    headers = {'Authorization': Basic + " " + base64}
    return requests.get(url, headers=headers)

def get_jobs()
    try:
        response = request(SAUCE_URL + SAUCE_USER + "/jobs?from=" + START_TIME)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print e
        sys.exit(1)

#Start
jobs_json = get_jobs.json()

#loop through each job in the list and process its assets
for id_key in jobs_json:
    print jobs_json[id_key]