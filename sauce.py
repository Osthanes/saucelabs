#!/usr/bin/python

import requests
import sys
import json
import time
import os
import base64
import urllib2
import logging

#ascii color codes for output
LABEL_GREEN = '\033[0;32m'
LABEL_RED = '\033[0;31m'
LABEL_COLOR = '\033[0;33m'
LABEL_NO_COLOR = '\033[0m'

#test result url
TEST_URL = "https://saucelabs.com/tests/%s"

#environment saucelabs variables
SAUCE_URL = "https://saucelabs.com/rest/v1/"
SAUCE_USER = os.environ.get('SAUCE_USERNAME')
SAUCE_ACCESS_KEY = os.environ.get('SAUCE_ACCESS_KEY')
START_TIME = os.environ.get('INIT_END_TIME')

def request(url):
    base64string = base64.encodestring('%s:%s' % (SAUCE_USER, SAUCE_ACCESS_KEY)).replace('\n', '')
    headers = {'Authorization': 'Basic %s' % base64string}
    return requests.get(url, headers=headers)

def get_jobs():
    try:
        response = request(SAUCE_URL + SAUCE_USER + "/jobs?from=" + START_TIME)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print e
        sys.exit(1)

def output_job(job):
    print LABEL_GREEN
    print "Job %s completed successfully." % job
    print "See details at: " + TEST_URL % job
    print LABEL_NO_COLOR

#Start
logging.captureWarnings(True)

jobs_json = get_jobs().json()

#loop through each job in the list and process its assets
for key in jobs_json:
    output_job(key["id"])
