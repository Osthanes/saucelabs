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
START_TIME = os.environ.get('INIT_START_TIME')

chunk_size = 1024

exit_flag = 0

def request(url):
    base64string = base64.encodestring('%s:%s' % (SAUCE_USER, SAUCE_ACCESS_KEY)).replace('\n', '')
    headers = {'Authorization': 'Basic %s' % base64string}
    return requests.get(url, headers=headers)

def download_log(url, job):
    base64string = base64.encodestring('%s:%s' % (SAUCE_USER, SAUCE_ACCESS_KEY)).replace('\n', '')
    headers = {'Authorization': 'Basic %s' % base64string}
    r = requests.get(url, headers=headers, stream=True)
    with open("selenium-server-" + job + ".log", 'wb') as fd:
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)

def download_video(url, job):
    base64string = base64.encodestring('%s:%s' % (SAUCE_USER, SAUCE_ACCESS_KEY)).replace('\n', '')
    headers = {'Authorization': 'Basic %s' % base64string}
    r = requests.get(url, headers=headers, stream=True)
    with open("video-" + job + ".flv", 'wb') as fd:
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)
            
def get_jobs():
    try:
        response = request(SAUCE_URL + SAUCE_USER + "/jobs?from=" + START_TIME)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print e
        sys.exit(1)
        
def get_job_status(job):
    try:
        response = request(SAUCE_URL + SAUCE_USER + "/jobs/" + job)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.exceptions.RequestException as e:
        print e
        sys.exit(1)
        
def get_job_assets(job):
    try:
        print "Getting selenium log for " + job
        download_log(SAUCE_URL + SAUCE_USER + "/jobs/" + job + "/assets/selenium-server.log", job)
        
        print "Getting video for " + job
        download_video(SAUCE_URL + SAUCE_USER + "/jobs/" + job + "/assets/video.flv", job)
    except requests.exceptions.RequestException as e:
        print e
        sys.exit(1)
        
def output_job(job):
    global exit_flag
    test_status = get_job_status(job)["consolidated_status"]
    if test_status == "passed": 
        print LABEL_GREEN
        print "Job %s passed successfully." % job
        print "See details at: " + TEST_URL % job
        print LABEL_NO_COLOR
    elif test_status == "complete":
        print LABEL_GREEN
        print "Job %s completed successfully." % job
        print "See details at: " + TEST_URL % job
        print LABEL_NO_COLOR
    #job failed
    else:
        print LABEL_RED
        print "There was problem with job %s." % job
        print "See details at: " + TEST_URL % job
        print LABEL_NO_COLOR
        exit_flag = 1
    
    #download selenium log
    get_job_assets(job)
    

#Start
logging.captureWarnings(True)

print "Getting jobs..."
jobs_json = get_jobs().json()

#loop through each job in the list and process its assets
print "Processing jobs..."
for key in jobs_json:
    output_job(key["id"])
    
#exit with appropriate status
sys.exit(exit_flag)
