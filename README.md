# Sauce Labs
## Simple extension to allow exection of Sauce Labs tests via the pipeline.


### Usage:
Provide Sauce Labs User Name in the text box provided and enter Sauce Access Key as an enviroment variable in the format `SAUCE_ACCESS_KEY : key`

In order to automatically run tests against the URL generated in the build stage, ensure that tests are configured to pull a URL from environment variables. Add two environment variables `CF_APP_NAME` with a blank value (delete any pre-filled data) and one with the key that the test code looks for (ie, `TEST_URL`) with no value as before.

The extension will check for the existance of a Gruntfile.js file and if found will attempt to run either `grunt test` or `grunt` if `grunt test` is not detected. 

If no Gruntfile.js is detected then it will default to `npm test`. 

Ensure that at least one of these commands kicks off tests or the job will fail.
