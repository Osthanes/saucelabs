#!/usr/bin/python

import os
import re
import sys

pattern = re.compile(r'\"test\": \"*\"')
if os.path.isfile("package.json"):
    with open("package.json", "r") as f:
        for line in f:
            if pattern.search(line):
                print "Found npm test script in package.json"
                exit(0)
    exit(1)
