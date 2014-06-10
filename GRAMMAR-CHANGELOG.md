Grammar Changelog
=================

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
