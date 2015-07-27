# Sauce Labs
## Simple extension to allow exection of Sauce Labs tests via the pipeline. Support for Java and Javascript testing.


### Usage:
Provide Sauce Labs User Name and Access Key in the text boxes provided.

In order to automatically run tests against the URL generated in the build stage, ensure that tests are configured to pull a URL from environment variables(namely `TEST_URL`). Add two environment variables `CF_APP_NAME` with a blank value (delete any pre-filled data) and one with the key `TEST_URL` with no value as before. This will the be the URL of the deployed app that the tests will run against.

Declare the following environment properties for the stage: `HOST` and `PORT`. These variables will be set in response to the use of Sauce Connect. Ensure that tests are configured to read from these variables and are not hardcoded.

Add the following command into the deploy job to ensure that the app URL is transferred to the test job: `export CF_APP_NAME="$CF_APP"` <strong>NOTE:</strong> Environment variables can only be transferred within a single stage (ie, from job to job), not from stage to stage.

Select whichever command best fits the test configuration (`npm test`, `grunt test`, `grunt`, `ant`, or `mvn`). If no selection fits the project enter a custom configuration in the provided command line and select "Custom".