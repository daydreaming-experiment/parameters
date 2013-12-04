Grammar v1
==========

Rules
-----

The grammar is defined by the following rules:

1. The parameters file contains pure [JSON](http://json.org/).
2. The root node in the file is a JSON object (`{}`) containing the following *mandatory* properties:
  * `version`: an *integer* defining the version of the parameters.
  * `nSlotsPerPoll`: an *integer* defining how many slots are allocated when a probe is created (see below the explanation about question groups and slots).
  * `questions`: a *list* of question objects (see below for a description of what question objects should contain).
  * Any other property on this root object is ignored.
3. A *question* object contains the following *mandatory* properties:
  * `name`: a *string* defining a name for the question (used to identify questions when retrieving the uploaded results).
  * `category`: a *string* representing the question's category.
  * `subCategory`: a *string* representing the question's sub-category (both are used for classification purposes when analysing results).
  * `slot`: a *string* representing both the question's group and group position (see below the explanation about question groups and slots).
  * `details`: a JSON *object* containing the details of the question, as detailed in the following rule.
4. A *detail* object contains the following *mandatory* properties:
  * `type`: a *string* representing the type of question asked; can be either `"MultipleChoice"`, `"Slider"`, or `"StarRating"` (star-ratings appear like sliders in the app, but behave in a discreet manner instead of continuous).
  * If `type` is `"MultipleChoice"`, the following properties are *mandatory*:
    * `text`: a *string* containing the actual question asked to the user.
    * `choices`: a *list* of *strings*, each one being a choice proposed to the user (the order is conserved).
  * If `type` is either `"Slider"` or `"StarRating"`, the following property is *mandatory*:
    * `subQuestions`: a *list* of sub-question objects, as detailed in the following rule.
5. A *sub-question* object contains the following *mandatory* properties:
  * `text`: a *string* containing the actual sub-question asked to the user.
  * `hints`: a *list* of at least two *strings*, which serves two purposes: the first and last items are shown as the extremes of a slider or star-rating, and the whole list of items is used as an indication of the user's choice as she sets the slider's progress or the star-rating's rating; this indication is only shown if the (misnamed) `showHints` property is `true`.
  * The following properties are *optional*:
    * `notApplyAllowed`: a *boolean*; if `true`, a check-box allowing the user to skip this specific sub-question will appear in the app; defaults to `false`.
    * `showHints`: a *boolean*; if `true`, show live indication of the user's rating as she makes her choice; defaults to `false`.
  * If the question `type` is `"Slider"`, the following property is *optional*:
    * `initialPosition`: an *integer* between `0` and `100` (included), defining the initial position of the selector on the slider when the question is asked; defaults to `0` (i.e. to the left).
  * If the question `type` is `"StarRating"`, the following properties are *optional*:
    * `numStars`: an positive *integer* defining the number of stars the rating would have if it were really displayed as a star-rating (and not as a discreet slider as is the case now); combined with `stepSize`, these two parameters define the number of discreet values the rating allows; defaults to `5`.
    * `stepSize`: a positive *float* defining the size of the interval between two discreet values; the total number of values allowed by the star-rating is `1 + ceiling(numStars  / stepSize)`; defaults to `0.5`.
    * `initialRating`: a *float* between `0.0` and `numStars` (included) defining the initial rating when the question is asked; this doesn't need to be a multiple of `stepSize`; defaults to `0.0` (i.e. to the left).


About question groups, slots, and positioning
---------------------------------------------

*Slots* and *groups* are used to express the way questions are selected and randomized when a probe is created. Basically, we want to be able to group questions together, randomize the *intra-group* order, randomize the *inter-group* order, and still have the possibility to put particular questions or groups of questions at specific positions in the question sequence (like the first or last).

So when creating a probe, the daydreaming app allocates `nSlotsPerPoll` *slots* to be filled, and `nSlotsPerPoll` *groups* of questions to be inserted in these slots (one group per slot). The slot into which a group is inserted can be either predefined or randomly selected (more about that below). Once the question groups are formed (more about that below, again), the predefined-position groups are inserted into their corresponding slots, and the random-position groups are inserted in random order into the remaining slots. Finally, each group of questions is itself internally randomized. This procedure allows for a broad range of question orderings and randomizations to be defined.

### Question selection and grouping

The parameters file assigns each question to a group that has either a predefined position or a random position. This is done thanks to the `slot` property, which serves to define both the group to which a question belongs and the given group's position (i.e. the slot: either predefined or random).

Here's how:

* All questions with an identical `slot` property belong to the same group; this is how groups are defined. There must be at least `nSlotsPerPoll` groups.
* `slot` is always a string, but if that string represents an *integer* (e.g. `"0"`, `"-1"`, or `"-2"`), then the corresponding group has a predefined position (so, respectively, the first, last, or penultimate slot). If `slot` does *not* represent an integer (e.g. `"A"` or `"B"`), the corresponding group will be randomly positioned.

Forming the question groups involves simply grouping together all the questions with identical `slot`, keeping *all* the predefined-position groups, and keeping only as many random-position groups as necessary (themselves randomly selected) to reach `nSlotsPerPoll` groups. So if the parameters file defines e.g. three predefined-position groups and four random-position groups, and `nSlotsPerPoll` is 5, two random-position groups are randomly selected among the available four, and the resulting five groups are fed to the slot-insertion process.

Note that if a group is to be inserted in the probe, *all* questions in that group will appear (i.e. there is no intra-group selection).

Final notes:
* Don't try stupid things with group positionning: if you define `nSlotsPerPoll` to be 5, and define a predefined-position group at position `"-7"`, I don't know what will happen (especially if there's another predefined-position group at position `"3"`).
* If there are more predefined-position groups than `nSlotsPerPoll`, I don't know what will happen either.
* `"1.0"`, `"1,0"`, `"2-1"`, etc., do **not** represent integers.
