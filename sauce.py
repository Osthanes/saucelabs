#!/usr/bin/python

import requests
import sys
import json
import time
import os
import base64
import urllib2
import logging
import hmac
from hashlib import md5
#from prettytable import PrettyTable

#ascii color codes for output
LABEL_GREEN = '\033[0;32m'
LABEL_YELLOW = '\033[4;33m'
LABEL_RED = '\033[0;31m'
LABEL_COLOR = '\033[0;33m'
LABEL_NO_COLOR = '\033[0m'
STARS = "**********************************************************************"

#test result url
TEST_URL = "https://saucelabs.com/jobs/%s?auth=%s"

#environment saucelabs variables
SAUCE_URL = "https://saucelabs.com/rest/v1/"
SAUCE_USER = os.environ.get('SAUCE_USERNAME')
SAUCE_ACCESS_KEY = os.environ.get('SAUCE_ACCESS_KEY')
START_TIME = os.environ.get('INIT_START_TIME')
DOWNLOAD_ASSETS = os.environ.get('DOWNLOAD_ASSETS')

chunk_size = 1024

exit_flag = 0

#browser test stat vars
FIREFOX_PASS = 0
FIREFOX_TOTAL = 0

CHROME_PASS = 0
CHROME_TOTAL = 0

IE_PASS = 0
IE_TOTAL = 0

SAFARI_PASS = 0
SAFARI_TOTAL = 0

JOB_DATA = "job_data_collection.json"

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
        append_job_json(response.content)
        return response_json
    except requests.exceptions.RequestException as e:
        print e
        sys.exit(1)
        
def get_job_assets(job):
    try:
        LOGGER.info("Getting selenium log for job: " + job)
        download_log(SAUCE_URL + SAUCE_USER + "/jobs/" + job + "/assets/selenium-server.log", job)
        
        LOGGER.info("Getting video for job: " + job)
        download_video(SAUCE_URL + SAUCE_USER + "/jobs/" + job + "/assets/video.flv", job)
    except requests.exceptions.RequestException as e:
        print e
        sys.exit(1)
        
def output_job(job):
    global exit_flag
    
    auth_key = hmac.new(SAUCE_USER + ":" + SAUCE_ACCESS_KEY, job, md5).hexdigest()
    
    test_info = get_job_status(job)
    
    browser = test_info["browser"]
    
    test_status = test_info["consolidated_status"]
    if test_status == "passed": 
        print LABEL_GREEN
        LOGGER.info("Job %s passed successfully." % job)
        LOGGER.info("See details at: " + TEST_URL % (job, auth_key))
        print LABEL_NO_COLOR
        analyze_browser_results(0, browser)
    elif test_status == "complete":
        print LABEL_GREEN
        LOGGER.info("Job %s completed successfully." % job)
        LOGGER.info("See details at: " + TEST_URL % (job, auth_key))
        print LABEL_NO_COLOR
        analyze_browser_results(0, browser)
    #for some reason job is still running
    elif test_status == "in progress":
        print LABEL_YELLOW
        LOGGER.info("Job %s is still in progress." % job)
        LOGGER.info("See details at: " + TEST_URL % (job, auth_key))
        print LABEL_NO_COLOR
    #job failed
    else:
        print LABEL_RED
        LOGGER.error("There was problem with job %s." % job)
        LOGGER.info("See details at: " + TEST_URL % (job, auth_key))
        print LABEL_NO_COLOR
        analyze_browser_results(1, browser)
        exit_flag = 1
    
    #download assets
    if DOWNLOAD_ASSETS == "true":
        get_job_assets(job)
    
def append_job_json(job_json):
    with open(JOB_DATA, 'a') as fd:
        fd.write(job_json + ",")
        fd.close()
    
def analyze_browser_results(status, browser):
    global FIREFOX_PASS
    global FIREFOX_TOTAL

    global CHROME_PASS
    global CHROME_TOTAL

    global IE_PASS
    global IE_TOTAL
    
    global SAFARI_PASS
    global SAFARI_TOTAL
    
    if browser == "firefox":
        if status == 0:
            FIREFOX_PASS += 1
        FIREFOX_TOTAL += 1
        
    if browser == "googlechrome":
        if status == 0:
            CHROME_PASS += 1
        CHROME_TOTAL += 1
        
    if browser == "iexplore":
        if status == 0:
            IE_PASS += 1
        IE_TOTAL += 1
        
    if browser == "safari":
        if status == 0:
            SAFARI_PASS += 1
        SAFARI_TOTAL += 1
    
def setup_logging():
    logger = logging.getLogger('pipeline')
    logger.setLevel(logging.INFO)

    # if logmet is enabled, send the log through syslog as well
    if os.environ.get('LOGMET_LOGGING_ENABLED'):
        handler = logging.handlers.SysLogHandler(address='/dev/log')
        logger.addHandler(handler)
        # don't send debug info through syslog
        handler.setLevel(logging.INFO)

    # in any case, dump logging to the screen
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    handler.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger

#Start
logging.captureWarnings(True)
LOGGER = setup_logging()

LOGGER.info("Getting jobs...")
jobs_json = get_jobs().json()

#loop through each job in the list and process its assets
with open(JOB_DATA, 'wb') as fd:
    fd.write("[")
    fd.close()
    
LOGGER.info("Processing jobs...")
for key in jobs_json:
    output_job(key["id"])
    
with open(JOB_DATA, 'a') as fd:
    fd.write("{}]")
    fd.close()    
    
#log test results
#print LABEL_GREEN
#print STARS
#results_table = PrettyTable(["Browser", "Jobs Succeeded", "Jobs Failed", "Total Jobs"])
#results_table.align["Browser"] = "l"
#results_table.add_row(["Firefox", FIREFOX_PASS, FIREFOX_TOTAL - FIREFOX_PASS, FIREFOX_TOTAL])
#results_table.add_row(["Google Chrome", CHROME_PASS, CHROME_TOTAL - CHROME_PASS, CHROME_TOTAL])
#results_table.add_row(["Internet Explorer", IE_PASS, IE_TOTAL - IE_PASS, IE_TOTAL])
#results_table.add_row(["Safari", SAFARI_PASS, SAFARI_TOTAL - SAFARI_PASS, SAFARI_TOTAL])
#print results_table
#print STARS
#print LABEL_NO_COLOR

 #log test results
print STARS
print LABEL_GREEN
print '%d out of %d jobs succeeded on Firefox.' % (FIREFOX_PASS, FIREFOX_TOTAL)
if FIREFOX_TOTAL - FIREFOX_PASS > 0:
    print LABEL_RED
    print '%d jobs failed.' % (FIREFOX_TOTAL - FIREFOX_PASS)
print LABEL_NO_COLOR

print STARS
print LABEL_GREEN
print '%d out of %d jobs succeeded on Google Chrome.' % (CHROME_PASS, CHROME_TOTAL)
if CHROME_TOTAL - CHROME_PASS > 0:
    print LABEL_RED
    print '%d jobs failed.' % (CHROME_TOTAL - CHROME_PASS)
print LABEL_NO_COLOR

print STARS
print LABEL_GREEN
print '%d out of %d jobs succeeded on Internet Explorer.' % (IE_PASS, IE_TOTAL)
if IE_TOTAL - IE_PASS > 0:
    print LABEL_RED
    print '%d jobs failed.' % (IE_TOTAL - IE_PASS)
print LABEL_NO_COLOR

print STARS
print LABEL_GREEN
print '%d out of %d jobs succeeded on Safari.' % (SAFARI_PASS, SAFARI_TOTAL)
if SAFARI_TOTAL - SAFARI_PASS > 0:
    print LABEL_RED
    print '%d jobs failed.' % (SAFARI_TOTAL - SAFARI_PASS)
print LABEL_NO_COLOR
print STARS

#exit with appropriate status
sys.exit(exit_flag)