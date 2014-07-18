Grammar Changelog
=================


Grammar v2.1
------------

Grammar `v2.1` is a backward compatible extension of grammar `v2`, with added fields. In the root node:
* `backendExpId`: a *string* defining the identity of the experiment for the backend.
* `backendDbName`: a *string* defining the name of the database to upload the results to in the backend.
* `expDuration`: an *integer* defining the duration before publication of results if users use the app as intented.
* `backendApiUrl`: a *string* defining the url of the backend API.
* `resultsPageUrl`: a *string* defining the url of the results page.
* `firstLaunch`: a JSON *object* containing a detailed description of the textual content of the views to be displayed at the first launch of the application as well as a description of the questionnaire questions they may contain.
1. `firstLaunch` is a JSON *object* with fields:
  * `welcomeText`: a *string* containing the text to be displayed in the Welcoming screen of the app.
  * `descriptionText`: a *string* containing the text to be displayed in the Description screen of the app.
  * `tipiQuestionnaire`: a JSON *object* defining the personality questionnaire to be displayed at first launch of the app.
2. In `firstLaunch`, there is a new `tipiQuestionnaire` *object* with fields:
  * `text`: a *string* containing the header description of the questionnaire.
  * `hintsForAllSubQuestions`: a *list* of *strings* containing the hints along the range of the slider answer of the questions of the questionnaire.
  * `subQuestions`: a *list* of JSON *objects* formatted as `tipiQuestion`s.
3. In `tipiQuestionnaire`, a `tipiQuestion` is an *object* with fields:
  * `text`: a *string* containing the question.
  * `initialPosition`: an optional *integer* defining the initial position of the slider.

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
