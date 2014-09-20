Grammar v3
==========

See [`GRAMMAR-CHANGELOG.md`](https://github.com/daydreaming-experiment/parameters/blob/master/GRAMMAR-CHANGELOG.md) for a description of the changes from the previous version.

Below is the full description of the grammar.

Rules
-----

The grammar is defined by the following rules (hold on, this is long!):

1. The parameters file contains pure [JSON](http://json.org/).
2. The root node in the file is a JSON object (`{}`) containing the following *mandatory* properties:
  * `version`: a *string* defining the version of the parameters.
  * `backendExpId`: a *string* defining the identity of the experiment for the backend.
  * `backendDbName`: a *string* defining the name of the database to upload the results to in the backend.
  * `expDuration`: an *integer* defining the duration before publication of results if users use the app as intended.
  * `backendApiUrl`: a *string* defining the url of the backend API.
  * `resultsPageUrl`: a *string* defining the url of the results page.
  * `schedulingMinDelay`: an *integer* defining the minimal delay between two probes (in seconds).
  * `schedulingMeanDelay`: an *integer* defining the average delay between two probes (in seconds).
  * `questions`: a *list* of question definition objects (see below for a description of what question definition objects should contain).
  * `sequences`: a *list* of sequence definition objects (see below for what they should contain).
  * `glossary`: a JSON *object* containing glossary definitions, where they key name is the definition name, and the key value is the definition body (both must be *strings*).
3. A *question definition* object contains the following *mandatory* properties:
  * `name`: a *string* defining a name for the question (used to reference questions when defining sequences); question names must be unique across questions.
  * `type`: a *string* representing the type of question asked; can be either `"multipleChoice"`, `"matrixChoice"`, `"autoList"`, `"manySliders"`, `"slider"`, or `"starRating"` (star-ratings appear like sliders in the app, but behave in a discreet manner instead of continuous).
  * `details`: a JSON *object* containing the details of the question, as detailed in the following rule.
4. A *details* object is the body of the question description; its content depend on the `type` property of the question:
  * If `type` is `"multipleChoice"`:
    * Mandatory fields:
      * `text`: a *string* containing the actual question asked to the user.
      * `choices`: a *list* of *strings*, each one being a choice proposed to the user (the order is conserved).
    * No optional fields
  * If `type` is `"matrixChoice"`:
    * Mandatory fields:
      * `text`: a *string* containing the actual question asked to the user.
      * `choices`: a *list* of *strings*, each one being a choice proposed to the user in the matrix (the order is conserved); for the moment choices can only be `"Home"`, `"Commuting"`, `"Work"`, `"Public space"`, or `"Outside"`, because those are the only items for which an icon is defined.
    * No optional fields
  * If `type` is `"autoList"`:
    * Mandatory fields:
      * `text`: a *string* containing the actual question asked to the user.
      * `hint`: a *string* defining what the drop-down list originally shows before the user starts typing in it.
      * `possibilities`: a *list* of *strings*, each one being a possibility proposed to the user in the drop-down list; those strings can contain tags, in a format described in a section below.
  * If `type` is `"manySliders"`:
    * Mandatory fields:
      * `text`: a *string* containing the actual question asked to the user.
      * `availableSliders`: a *list* of *strings* defining all the initially available slider titles; these can have tags as in the `autoList` question.
      * `defaultSliders`: a *list* of *strings* defining the sliders that will appear the first time the user answers this question (subsequently his editions will apply); each item here must be present in `availableSliders`.
      * `hints`: a *list* of at least two *strings*, which serves two purposes: the first and last items are shown as the extremes of on each slider, and the whole list of items is used as an indication of the user's choice as she sets the slider's progress; this indication is only shown if the `showLiveIndication` property is `true`.
      * `addItemHint`: a *string* defining what the drop-down list in edit-mode originally shows before the user starts typing in it.
      * `dialogText`: a *string* defining the text of the explanation dialog that appears when the user enters edit mode in the question.
    * Optional field:
      * `showLiveIndication`: a *boolean*; if `true`, show live indication of the user's rating as she makes her choice on sliders; defaults to `false`.
      * `initialPosition`: an *integer* between `0` and `100` (included), defining the initial position of the selector on the sliders when the question is asked; defaults to `0` (i.e. to the left).
  * If `type` is `"slider"` or `"starRating"`:
    * There is a single mandatory field, `subQuestions`: it contains a *list* of sub-question objects; those sub-questions have the following *mandatory* fields:
      * `text`: a *string* containing the actual sub-question asked to the user.
      * `hints`: a *list* of at least two *strings*, which are used just like the hints in `manySliders`; note that here again, live indication is only shown if the `showLiveIndication` property is `true`.
    * sub-questions have the following *optional* properties:
      * `notApplyAllowed`: a *boolean*; if `true`, a check-box allowing the user to skip this specific sub-question will appear in the app; defaults to `false`.
      * `showLiveIndication`: a *boolean*; if `true`, show live indication of the user's rating as she makes her choice; defaults to `false`.
    * If the question `type` is `"slider"`, the following property is *optional* in sub-questions:
      * `initialPosition`: an *integer* between `0` and `100` (included), defining the initial position of the selector on the slider when the question is asked; defaults to `0` (i.e. to the left).
    * If the question `type` is `"starRating"`, the following properties are *optional*:
      * `numStars`: a positive *integer* defining the number of stars the rating would have if it were really displayed as a star-rating (and not as a discreet slider as is the case now); combined with `stepSize`, these two parameters define the number of discreet values the rating allows; defaults to `5`.
      * `stepSize`: a positive *float* defining the size of the interval between two discreet values; the total number of values allowed by the star-rating is `1 + ceiling(numStars  / stepSize)`; defaults to `0.5`.
      * `initialRating`: a *float* between `0.0` and `numStars` (included) defining the initial rating when the question is asked; this doesn't need to be a multiple of `stepSize`; defaults to `0.0` (i.e. to the left).
5. A *sequence definition* object is used to define sequences, which represent any list of questions, with additional positioning parameters. Such an object has the following mandatory fields:
  * `name`: a *string* defining the name of the sequence, as it will appear in the uploaded results (e.g. `morningQuestionnaire`, or `personalityQuestionnaireSODAS`).
  * `type`: a *string* defining the type of the sequence, which can be either `probe`, `beginEndQuestionnaire`, `morningQuestionnaire`, or `eveningQuestionnaire`.
  * `intro`: a *string* defining the text that will appear at the top of all questions in the sequence.
  * `nSlots`: an *integer* defining the number of slots available in the sequence for `pageGroups` (see below the explanation about positioning).
  * `pageGroups`: a *list* of *pageGroup* objects, as defined in the following rule.
6. A *pageGroup* object represents a block of screens in the app. It contains the following fields (all mandatory):
  * `name`: a *string* defining the name of the page group, as it will appear in the uploaded results (e.g. `context`, or `thoughts`). Names must be unique across page groups, as they're used for positioning.
  * `friendlyName`: a *string* defining a name to be shown to the user, which can be used in the future to display a progress bar during a sequence.
  * `position`: a *position* object defining how the page group is positioned in the sequence. See rule 9 for what positions look like.
  * `nSlots`: an *integer* defining the number of slots available in the page group for `page` objects (see below the explanation about positioning).
  * `pages`: a *list* of *page* objects, as defined in the following rule.
7. A *page* object represents a bunch of questions shown on a single screen in the app. It contains the following fields (all mandatory):
  * `name`: a *string* defining the name of the page, as it will appear in the uploaded results (e.g. `context.location`, or `thoughts.future`). Names must be unique across pages, as they're used for positioning.
  * `position`: a *position* object defining how the page is positioned in the page group. See rule 9 for what positions look like.
  * `nSlots`: an *integer* defining the number of slots available in the page for `question reference` objects (see below the explanation about positioning).
  * `questions`: a *list* of *question references*, as defined in the following rule.
8. A *question reference* points to a question defined in the `questions` list defined at the top of the file, and positions this question. It has the following fields (all mandatory):
  * `name`: a *string* defining the name of question reference (note, it's the name of the *reference* to the question, not the name of the question itself). Names must be unique across pages, as they're used for positioning.
  * `questionName`: a *string* corresponding to a name of one of the questions defined in the `questions` list at the top of this file. This is the question that will be shown, of course. Note that this appears in the uploaded results, whereas the name of the question reference (field right above this one) does not appear in the results. Note that `matrixChoice`, `manySliders`, and `autoList` question are what we call "single-page" questions: they must be alone in their page.
  * `position`: a *position* object defining how the question is positioned in the page. See rule 9 below for what positions look like.
9. A *position* object defines how items are positioned at each level of the hierarchy in the sequence. See below for a detailed explanation on how positioning is done. These objects can have the following fields:
  * `fixed`: an *integer* defining the fixed position of the item (can be positive or negative).
  * `floating`: a *string* defining the floating group of the item.
  * `after`: a *string* corresponding the *name* of an item at the same hierarchy level. For instance, ff you're positioning a question, must be the name of a question.
  * `bonus`: a *boolean* defining if this item is bonus or not. Only pages and page groups can be bonus, *not* question references.
  * `fixed`, `floating`, and `after` are all mutually exclusive: only one of them can be defined, and exactly one must be defined. `bonus` is optional, and is compatible with any of `fixed`, `floating`, and `after` (provided that your item is a page or a page group, but not a question reference). Note that having the first question of a probe appear as `bonus` is pretty bad UI (the bonus dialog will appear before anything else), so you should try to avoid that possibility.

About sequences
---------------

*Sequences* are a generalized form of what the previous grammar versions called *probes*. Basically, they represent a set of questions (by referencing the questions defined separately in the first part of the parameters file), with three levels of grouping to enable fine-grained positioning and randomization: *questions* are grouped into *pages*, which represent a single screen in the app (note that the `matrixChoice`, `manySliders`, and `autoList` questions are single-page: they must be alone in their page). *Pages* are grouped into *pageGroups*, representing blocks of screens (like context-related questions, or thoughts-related questions). Finally, a sequence is made of `pageGroups`.

Sequences have a type, which defines how they're used by the app: the type tells the app if we're talking about a probe, about a morning questionnaire, an evening questionnaire, or a beginning/ending questionnaire. For the moment, there should be:
* A single sequence of type `probe`, which should also be named `"probe"`
* A single sequence of type `morningQuestionnaire`, also named `morningQuestionnaire`
* A single sequence of type `eveningQuestionnaire`, also named `eveningQuestionnaire`
* As many sequences as you want with type `beginEndQuestionnaire`, each named as you like

Positioning of items inside sequences is a bit involved. See the description in the following section.

About slots and positioning
---------------------------

*Slots* are used to express the way items are selected and randomized when a sequence is created. Basically, we want to be able to group questions together in great question groups, in pages containing a bunch of questions, and randomize all this at every possible level, while still being able to position questions at particular positions, or after other questions.

Enter *slots*. Imagine you have a list of items (they can be questions, pages, or page groups), and you want to define their order. First, you define the number of slots your final order will have. Each slot will contain a bunch of items, and the items inside a slot are randomized. The position of each item (which slot it falls into) can be either "fixed" or "floating": if "fixed", an item will go in the slot indicated by its fixed position (this position can be negative, counting from the end as in python). So all items with position `"fixed": 0` will be put in the very first slot (and then randomized inside the slot). On the other hand, "floating" items are grouped together with the other items having the same "floating" position, randomized, and put in any free slot once all the "fixed" groups have been positioned. So all items with position `"floating": "A"` will be grouped together, randomized, and put in a free slot once all "fixed" items are positioned. All items with position `"floating": "B"` will also be grouped, randomized, and put in a free slot.

Note that "floating" items are positioned in the free slots left by "fixed" items. So for instance, if you allocate 5 slots and you have 3 different "fixed" positions (say you have 12 items, each assigned to positions 0, 1, and -1), and 4 different "floating" positions, then only 2 of your 4 "floating" groups will be used (selected randomly), since there's only two free slots after positioning all the "fixed" items. This is useful if you want some questions to appear sometimes but not always.

Items can also be positioned "after" other items (by naming the item after which the current one should appear). As with "fixed" and "floating", all items coming "after" a given parent item are grouped together, randomized, and inserted after the parent item in that order. Note that this operation comes *after* positioning of "fixed" and "floating" items, so these items don't count in the number of slots you defined (they are inserted "between" slots, so to speak). This operation works recursively, i.e. you can position an item after an item positioned after another item, etc. The grouping also works recursively: you can have items `d` and `e` after `b`, and `c` and `b` after `a`, then you'll get `a->c->b->e->d` or `a->c->b->d->e` or `a->b->d->e->c` or `a->b->e->d->c`), although I don't see how that could ever be useful. Note that you can position an item after another item even if you don't know its final position: you position after a *name*, not in a slot (and that's the whole point). You can position item `a` after item `b`, and set item `b` to position `"floating": "foo"`, and wherever that floating item ends up it will always be followed by item `a`.

This randomizing and positioning works at each level of the sequence hierarchy: page groups are positioned like that in the sequence, pages are positioned like that in page group, and questions are positioned like that in pages, and that's why each item at each level has its own `position` field. So this gives you a lot of liberty.

Finally, page groups and pages can also be "bonus" if so defined in their `position` field, i.e. the user can skip them. Setting a page group to bonus will set all pages inside to bonus. When the app is asking a sequence to the user and it meets a bonus item, it asks the user if she want bonus questions or not, and then either skips all bonus questions or shows them all. Note that questions themselves can't be bonus, only pages or page groups.

Final notes:
* Don't try stupid things with slot positioning: if you define `nSlots` to be 5, and define a fixed-position item at position `"-7"`, I don't know what will happen (especially if there's another fixed-position item at position `"3"`).
* There must always be enough slots to fit all the fixed-position items: so the number of different fixed-positions must be less than or equal to `nSlots`.

About tags
----------

`manySliders` and `autoList` question types define possibilities that can be "tagged". Tags are like keywords for search: when the user searches for a string in an `autoList` drop-down list, if his query matches a tag, the corresponding possibility is shown (with its tags). That way I can type in "book" and find "reading" (I can also type in "rea" to find "reading"). Tags are defined as a comma-separated list of items after the main text of a possibility: `"main text of the possibility|tag1, tag2, tag3"`. They can have spaces, as long as they're separated by commas. Tags are optional (simply omit the `|` and what comes after it).
