Grammar Changelog
=================


Grammar v2.1
------------

Grammar `v2.1` is a backward compatible extension of grammar `v2`
Additional fields in the root:
* `expId`: a *string* defining the identity of the experiment.
* `dbName`: a *string* defining the name of the database to upload the results to.
* `expDuration`: an *integer* defining the duration before publication of results if users use the app as intented.
* `urlBackendApi`: a *string* defining the url of the backend API.
* `urlResultsPage`: a *string* defining the url of the results page.
* `firstLaunch`: a JSON *object* containing a detailed description of the textual content of the views to be displayed at the first launch of the application as well as a description of the questionnaire questions they may contain.
1. `firstLaunch`: a JSON *object* with fields:
 * `welcomeText`: a *string* containing the text to be displayed in the Welcoming screen of the application.
 * `descriptionText`: a *string* containing the text to be displayed in the Description screen of the application.
 * `tipiQuestionnaire`: a JSON *object* defining the personality questionnaire to be displayed at first launch of the app.
2. `tipiQuestionnaire`: a JSON *object* with fields:
  * `text`: a string containing the header description of the questionnaire.
  * `hintsForAllSubQuestions`: a *list* of *string* containing the hints along the range of the slider answer of the questions of the questionnaire.
  * `subQuestions`: a *list* of JSON *object* tipiQuestion
3. `tipiQuestion`: a JSON *object* with fields:
   * `text`: a *string* containing the question
   * `initialPosition`: an *integer* in [0,100] declaring the initial position of the slider.
      
Grammar v2
----------

Grammar `v2` is essentially the same as grammar `v1`, with the following four changes (the first three render it backwards-incompatible):
* `version` in the root object is now a *string*, allowing for version names like `test-1`, `qa-1`, `prod-1`.
* The misnamed `showHints` has been renamed to `showLiveIndication`.
* The misnamed `nSlotsPerPoll` has been renamed to `nSlotsPerProbe`.
* There are two new *mandatory* properties in the root object:
  * `schedulingMinDelay`: an *integer* defining the minimal delay between two probes (in seconds).
  * `schedulingMeanDelay`: an *integer* defining the average delay between two probes (in seconds).

Grammar v1
----------

First formalised version of the grammar.
