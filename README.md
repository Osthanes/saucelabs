# Sauce Labs
## Simple extension to allow exection of Sauce Labs tests via the pipeline.


### Usage:
Provide Sauce Labs User Name and Access Key in the text boxes provided.

In order to automatically run tests against the URL generated in the build stage, ensure that tests are configured to pull a URL from environment variables(namely `TEST_URL`). Add two environment variables `CF_APP_NAME` with a blank value (delete any pre-filled data) and one with the key `TEST_URL` with no value as before. This will the be the URL of the deployed app that the tests will run against.

Uncomment whichever command best fits the test configuration (`npm test`, `grunt test`, `grunt`) or add a custom test execution command at the end. `npm install` is run before test execution so it is not necessary to add.
