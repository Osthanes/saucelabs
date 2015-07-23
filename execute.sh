#!/bin/bash

#********************************************************************************
# Copyright 2014 IBM
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#********************************************************************************

#############
# Colors    #
#############
export green='\e[0;32m'
export red='\e[0;31m'
export label_color='\e[0;33m'
export no_color='\e[0m' # No Color

##################################################
# Simple function to only run command if DEBUG=1 # 
### ###############################################
debugme() {
  [[ $DEBUG = 1 ]] && "$@" || :
}

set +e
set +x 

if [ -z "${SAUCE_USERNAME}" ]; then
    echo -e "${red}No SAUCE_USERNAME defined, please enter your username in the stage configuration.${no_color}"
    exit 1     
fi 

if [ -z "${SAUCE_ACCESS_KEY}" ]; then 
    echo -e "${red}No SAUCE_ACCESS_KEY defined, please either select for the service to be added, or define SAUCE_ACCESS_KEY in the stage configuration${no_color}"
    exit 1     
fi 

debugme echo "SAUCE_ACCESS_KEY: ${SAUCE_ACCESS_KEY}"
debugme echo "USER_ID: ${SAUCE_USERNAME}"

#Run tests
npm install

echo "Starting test"

#check for gruntfile
if [ -f Gruntfile.js ]; then
    #run grunt test if task is registered
    if grep -q "grunt.registerTask('test'," Gruntfile.js; then
        grunt test
        RESULT=$?
        if [ $RESULT -ne 0 ]; then
            exit 1
        fi
    else
    #otherwise run default
        grunt
        RESULT=$?
        if [ $RESULT -ne 0 ]; then
            exit 1
        fi
    fi
else
    npm test
    RESULT=$?
    if [ $RESULT -ne 0 ]; then
        exit 1
    fi
fi