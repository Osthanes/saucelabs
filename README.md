# Sauce Labs
## Simple extension to allow exection of Sauce Labs tests via the pipeline. Support for Java and Javascript testing.


### Usage:
Provide Sauce Labs User Name and Access Key in the text boxes provided.

The follwing environment variables will need to be added:
* `CF_APP_NAME`: The name of the app that will be pulled from the deploy job. Leave empty.
* `APP_URL`: The URL of the deployed app that will be set from Cloud Foundry. Ensure the test code is configured to read in this value for the URL and are not hardcoded. If this is known then populate with the URL; if not it will be configured from the deploy the job.

In order to automatically run tests against the URL generated in the deploy stage, ensure that tests are configured to pull a URL from the environment variables (namely `TEST_URL`).

Add the following command into the deploy job to ensure that the app URL is transferred to the test job: `export CF_APP_NAME="$CF_APP"` <strong>NOTE:</strong> Environment variables can only be transferred within a single stage (ie, from job to job), not from stage to stage.

Select whichever command best fits the test configuration (`npm test`, `grunt test`, `grunt`, `ant`, or `mvn`). If no selection fits the project enter a custom configuration in the provided command line and select "Custom".

To best utilize the Test Reporting tab for Node applications, configure Mocha to use the `mocha-jenkins-reporter` as this will generate correctly formatted xunit output for the reporter. Standard JUnit reporting will work for Java.

See [Example IBM Bluemix Pipeline with Sauce Labs](https://github.com/Puquios/sauce-labs_setup) for a pre-configured pipeline.
