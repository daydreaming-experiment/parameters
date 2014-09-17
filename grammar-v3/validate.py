#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Test a parameters file to check it follows grammar v3."""


import json
import unittest
import os
import sys
from random import shuffle
from pprint import pprint


class ParametersFileTestCase(unittest.TestCase):

    def setUp(self):
        self.f = open(filename, 'r')

    def tearDown(self):
        self.f.close()


class JSONTestCase(ParametersFileTestCase):

    description = 'Checking the file is proper JSON'

    def test_is_json(self):
        try:
            json.load(self.f)
        except ValueError:
            self.fail('{} is not valid JSON!'.format(filename))


class LoadedTestCase(ParametersFileTestCase):

    type_names = {int: 'an integer',
                  float: 'a float',
                  str: 'a string',
                  dict: 'a JSON object',
                  list: 'a list',
                  bool: 'a boolean'}
    error_in = "{0} has no '{1}' property"
    error_type = "'{1}' (in {0}) is not {2}"
    error_in_list = "{1} (={2}) (in {0}) is not in {3}"
    error_true = "{1} (in {0})"
    error_empty_list = "'{1}' (in {0}) is an empty list"
    warn_default = "You defined '{1}' (in {0}) but set it to its default value"

    def setUp(self):
        super(LoadedTestCase, self).setUp()
        self.params = json.load(self.f)

    def checkInstance(self, obj, attr_name, tipe, optional=False):
        if not optional or obj.__getattribute__(attr_name) is not None:
            err = self.error_type.format(obj.name_err, attr_name,
                                         self.type_names[tipe])
            attr = obj.__getattribute__(attr_name)
            self.assertIsInstance(attr, tipe, err)

    def checkIn(self, obj, container, attr_name, optional=False):
        if not optional:
            err = self.error_in.format(obj.name_err, attr_name)
            self.assertIn(attr_name, container, err)
        return container.get(attr_name, None)

    def checkInList(self, obj, container, value, value_name,
                    container_name=None):
        err = self.error_in_list.format(obj.name_err, value_name,
                                        value, container_name or container)
        self.assertIn(value, container, err)

    def checkTrue(self, obj, assertion, msg):
        err = self.error_true.format(obj.name_err, msg)
        self.assertTrue(assertion, err)


class TypesTestCase(LoadedTestCase):

    description = ('Checking all the attributes are present '
                   'and have the right types')

    def test_types(self):
        parameters = Parameters(self, self.params)
        parameters.test_types()


class ValuesTestCase(LoadedTestCase):

    description = 'Checking all the values are correct'

    def test_values(self):
        parameters = Parameters(self, self.params)
        parameters.test_values()


class Parameters:

    def __init__(self, tc, loaded):
        # The test case
        self.tc = tc

        # Error message suffix
        self.name_err = 'root of parameters'

        # Fill members
        self.version = tc.checkIn(self, loaded, 'version')
        self.backendExpId = tc.checkIn(self, loaded, 'backendExpId')
        self.backendDbName = tc.checkIn(self, loaded, 'backendDbName')
        self.expDuration = tc.checkIn(self, loaded, 'expDuration')
        self.backendApiUrl = tc.checkIn(self, loaded, 'backendApiUrl')
        self.resultsPageUrl = tc.checkIn(self, loaded, 'resultsPageUrl')
        self.schedulingMinDelay = tc.checkIn(self, loaded,
                                             'schedulingMinDelay')
        self.schedulingMeanDelay = tc.checkIn(self, loaded,
                                              'schedulingMeanDelay')
        self.questions = tc.checkIn(self, loaded, 'questions')
        self.sequences = tc.checkIn(self, loaded, 'sequences')

    def kiddos(self, test_name):
        for i, q in enumerate(self.questions):
            qq = Question(self.tc, i, q, self)
            qq.__getattribute__(test_name)()

        #for s in self.sequences:
            #ss = Sequence(tc, self, s)
            #ss.__getattribute__(test_name)()

    def test_types(self):
        self.tc.checkInstance(self, 'version', str)
        self.tc.checkInstance(self, 'backendExpId', str)
        self.tc.checkInstance(self, 'backendDbName', str)
        self.tc.checkInstance(self, 'expDuration', int)
        self.tc.checkInstance(self, 'backendApiUrl', str)
        self.tc.checkInstance(self, 'resultsPageUrl', str)
        self.tc.checkInstance(self, 'schedulingMinDelay', int)
        self.tc.checkInstance(self, 'schedulingMeanDelay', int)
        self.tc.checkInstance(self, 'questions', list)
        self.tc.checkInstance(self, 'sequences', list)
        self.kiddos('test_types')

    def test_values(self):
        self.tc.checkTrue(self, self.expDuration >= 1,
                          'expDuration must be at least one day')
        self.tc.checkTrue(self,
                          self.schedulingMinDelay < self.schedulingMeanDelay,
                          'schedulingMinDelay should be < schedulingMeanDelay')
        self.tc.checkTrue(self, self.schedulingMinDelay > 60,
                          'schedulingMinDelay should be at least 1 minute')
        self.tc.checkTrue(self, self.schedulingMeanDelay > 5 * 60,
                          'schedulingMinDelay should be at least 5 minutes')
        self.kiddos('test_values')


class Choice:

    def __init__(self, tc, i, loaded, parent):
        # The test case
        self.tc = tc

        # Error message suffix
        self.name_err = 'choice #{} in '.format(i) + parent.name_err

        # Fill members
        self.string = loaded

    def test_types(self):
        self.tc.checkInstance(self, 'string', str)


class MatrixChoice:

    possible_choices = {'Home', 'Commuting', 'Outside',
                        'Public place', 'Work'}

    def __init__(self, tc, i, loaded, parent):
        # The test case
        self.tc = tc

        # Error message suffix
        self.name_err = 'choice #{} in '.format(i) + parent.name_err

        # Fill members
        self.string = loaded

    def test_types(self):
        self.tc.checkInstance(self, 'string', str)

    def test_values(self):
        self.tc.checkInList(self, self.possible_choices, self.string,
                            'this matrix choice')


class Hint:

    def __init__(self, tc, i, loaded, parent):
        # The test case
        self.tc = tc

        # Error message suffix
        self.name_err = 'hint #{} in '.format(i) + parent.name_err

        # Fill members
        self.string = loaded

    def test_types(self):
        self.tc.checkInstance(self, 'string', str)

    def test_values(self):
        # Nothing to test
        pass


class Slider:

    def __init__(self, tc, i, loaded, parent):
        # The test case
        self.tc = tc

        # Error message suffix
        self.name_err = 'slider #{} in '.format(i) + parent.name_err

        # Fill members
        self.string = loaded

    def test_types(self):
        self.tc.checkInstance(self, 'string', str)

    def test_values(self):
        self.tc.checkTrue(self, self.string.count('|') <= 1,
                          'there must be at most one "|"')


class Possibility:

    def __init__(self, tc, i, loaded, parent):
        # The test case
        self.tc = tc

        # Error message suffix
        self.name_err = 'possibility #{} in '.format(i) + parent.name_err

        # Fill members
        self.string = loaded

    def test_types(self):
        self.tc.checkInstance(self, 'string', str)

    def test_values(self):
        self.tc.checkTrue(self, self.string.count('|') <= 1,
                          'there must be at most one "|"')


class MultipleChoiceDetails:

    def __init__(self, tc, loaded, parent):
        # The test case
        self.tc = tc

        # Error message suffix
        self.name_err = 'multipleChoiceDetails in ' + parent.name_err

        # Fill members
        self.text = tc.checkIn(self, loaded, 'text')
        self.choices = tc.checkIn(self, loaded, 'choices')

    def kiddos(self, test_name):
        for i, c in enumerate(self.choices):
            cc = Choice(self.tc, i, c, self)
            cc.__getattribute__(test_name)()

    def test_types(self):
        self.tc.checkInstance(self, 'text', str)
        self.tc.checkInstance(self, 'choices', list)
        self.kiddos('test_types')

    def test_values(self):
        self.tc.checkTrue(self, len(self.choices) >= 2,
                          'there must be at least two choices')
        # No kiddos


class MatrixChoiceDetails:

    def __init__(self, tc, loaded, parent):
        # The test case
        self.tc = tc

        # Error message suffix
        self.name_err = 'matrixChoiceDetails in ' + parent.name_err

        # Fill members
        self.text = tc.checkIn(self, loaded, 'text')
        self.choices = tc.checkIn(self, loaded, 'choices')

    def kiddos(self, test_name):
        for i, m in enumerate(self.choices):
            mm = MatrixChoice(self.tc, i, m, self)
            mm.__getattribute__(test_name)()

    def test_types(self):
        self.tc.checkInstance(self, 'text', str)
        self.tc.checkInstance(self, 'choices', list)
        self.kiddos('test_types')

    def test_values(self):
        self.tc.checkTrue(self, len(self.choices) >= 2,
                          'there must be at least two choices')
        self.kiddos('test_values')


class AutoListDetails:

    def __init__(self, tc, loaded, parent):
        # The test case
        self.tc = tc

        # Error message suffix
        self.name_err = 'autoListDetails in ' + parent.name_err

        # Fill members
        self.text = tc.checkIn(self, loaded, 'text')
        self.hint = tc.checkIn(self, loaded, 'hint')
        self.possibilities = tc.checkIn(self, loaded, 'possibilities')

    def kiddos(self, test_name):
        for i, p in enumerate(self.possibilities):
            pp = Possibility(self.tc, i, p, self)
            pp.__getattribute__(test_name)()

    def test_types(self):
        self.tc.checkInstance(self, 'text', str)
        self.tc.checkInstance(self, 'hint', str)
        self.tc.checkInstance(self, 'possibilities', list)
        self.kiddos('test_types')

    def test_values(self):
        self.tc.checkTrue(self, len(self.possibilities) >= 2,
                          'there must be at least two possibilities')
        self.kiddos('test_values')


class ManySlidersDetails:

    def __init__(self, tc, loaded, parent):
        # The test case
        self.tc = tc

        # Error message suffix
        self.name_err = 'manySlidersDetails in ' + parent.name_err

        # Fill members
        self.text = tc.checkIn(self, loaded, 'text')
        self.availableSliders = tc.checkIn(self, loaded, 'availableSliders')
        self.defaultSliders = tc.checkIn(self, loaded, 'defaultSliders')
        self.hints = tc.checkIn(self, loaded, 'hints')
        self.addItemHint = tc.checkIn(self, loaded, 'addItemHint')
        self.dialogText = tc.checkIn(self, loaded, 'dialogText')
        self.showLiveIndication = tc.checkIn(self, loaded,
                                             'showLiveIndication', True)
        self.initialPosition = tc.checkIn(self, loaded, 'initialPosition',
                                          True)

    def kiddos(self, test_name):
        for i, s in enumerate(self.availableSliders):
            ss = Slider(self.tc, i, s, self)
            ss.__getattribute__(test_name)()
        for i, s in enumerate(self.defaultSliders):
            ss = Slider(self.tc, i, s, self)
            ss.__getattribute__(test_name)()
        for i, h in enumerate(self.hints):
            hh = Hint(self.tc, i, h, self)
            hh.__getattribute__(test_name)()

    def test_types(self):
        self.tc.checkInstance(self, 'text', str)
        self.tc.checkInstance(self, 'availableSliders', list)
        self.tc.checkInstance(self, 'defaultSliders', list)
        self.tc.checkInstance(self, 'hints', list)
        self.tc.checkInstance(self, 'addItemHint', str)
        self.tc.checkInstance(self, 'dialogText', str)
        self.tc.checkInstance(self, 'showLiveIndication', bool, True)
        self.tc.checkInstance(self, 'initialPosition', int, True)
        self.kiddos('test_types')

    def test_values(self):
        self.tc.checkTrue(self, len(self.hints) >= 2,
                          'there must be at least two hints')
        self.tc.checkTrue(self, 0 <= self.initialPosition <= 100,
                          'initialPosition must be between 0 and 100')
        for ds in self.defaultSliders:
            self.tc.checkInList(self, self.availableSliders, ds,
                                'this defaultSlider', 'availableSliders')
        self.kiddos('test_values')


class SliderSubQuestion:

    def __init__(self, tc, i, loaded, parent):
        # The test case
        self.tc = tc

        # Error message suffix
        self.name_err = 'subQuestion #{} in '.format(i) + parent.name_err

        # Fill members
        self.text = tc.checkIn(self, loaded, 'text')
        self.hints = tc.checkIn(self, loaded, 'hints')
        self.notApplyAllowed = tc.checkIn(self, loaded, 'notApplyAllowed',
                                          True)
        self.showLiveIndication = tc.checkIn(self, loaded,
                                             'showLiveIndication', True)
        self.initialPosition = tc.checkIn(self, loaded, 'initialPosition',
                                          True)

    def kiddos(self, test_name):
        for i, h in enumerate(self.hints):
            hh = Hint(self.tc, i, h, self)
            hh.__getattribute__(test_name)()

    def test_types(self):
        self.tc.checkInstance(self, 'text', str)
        self.tc.checkInstance(self, 'hints', list)
        self.tc.checkInstance(self, 'notApplyAllowed', bool, True)
        self.tc.checkInstance(self, 'showLiveIndication', bool, True)
        self.tc.checkInstance(self, 'initialPosition', int, True)
        self.kiddos('test_types')

    def test_values(self):
        self.tc.checkTrue(self, len(self.hints) >= 2,
                          'there must be at least two hints')
        self.tc.checkTrue(self, 0 <= self.initialPosition <= 100,
                          'initialPosition must be between 0 and 100')
        # No kiddos


class SliderDetails:

    def __init__(self, tc, loaded, parent):
        # The test case
        self.tc = tc

        # Error message suffix
        self.name_err = 'sliderDetails in ' + parent.name_err

        # Fill members
        self.subQuestions = tc.checkIn(self, loaded, 'subQuestions')

    def kiddos(self, test_name):
        for i, s in enumerate(self.subQuestions):
            ss = SliderSubQuestion(self.tc, i, s, self)
            ss.__getattribute__(test_name)()

    def test_types(self):
        self.kiddos('test_types')

    def test_values(self):
        self.kiddos('test_values')


class StarRatingSubQuestion:

    def __init__(self, tc, i, loaded, parent):
        # The test case
        self.tc = tc

        # Error message suffix
        self.name_err = 'subQuestion #{} in '.format(i) + parent.name_err

        # Fill members
        self.text = tc.checkIn(self, loaded, 'text')
        self.hints = tc.checkIn(self, loaded, 'hints')
        self.notApplyAllowed = tc.checkIn(self, loaded, 'notApplyAllowed',
                                          True)
        self.showLiveIndication = tc.checkIn(self, loaded,
                                             'showLiveIndication', True)
        self.numStars = tc.checkIn(self, loaded, 'numStars', True)
        self.stepSize = tc.checkIn(self, loaded, 'stepSize', True)
        self.initialRating = tc.checkIn(self, loaded, 'initialRating', True)

    def kiddos(self, test_name):
        for i, h in enumerate(self.hints):
            hh = Hint(self.tc, i, h, self)
            hh.__getattribute__(test_name)()

    def test_types(self):
        self.tc.checkInstance(self, 'text', str)
        self.tc.checkInstance(self, 'hints', list)
        self.tc.checkInstance(self, 'notApplyAllowed', bool, True)
        self.tc.checkInstance(self, 'showLiveIndication', bool, True)
        self.tc.checkInstance(self, 'numStars', int, True)
        self.tc.checkInstance(self, 'stepSize', float, True)
        self.tc.checkInstance(self, 'initialRating', float, True)
        self.kiddos('test_types')

    def test_values(self):
        self.tc.checkTrue(self, len(self.hints) >= 2,
                          'there must be at least two hints')
        self.tc.checkTrue(self, 0 <= self.initialRating <= self.numStars,
                          'initialRating must be between 0 and numStars')
        self.tc.checkTrue(self, 0 < self.numStars, 'numStars must be positive')
        self.tc.checkTrue(self, 0 < self.stepSize, 'stepSize must be positive')
        # No kiddos


class StarRatingDetails:

    def __init__(self, tc, loaded, parent):
        # The test case
        self.tc = tc

        # Error message suffix
        self.name_err = 'starRatingDetails in ' + parent.name_err

        # Fill members
        self.subQuestions = tc.checkIn(self, loaded, 'subQuestions')

    def kiddos(self, test_name):
        for i, s in enumerate(self.subQuestions):
            ss = StarRatingSubQuestion(self.tc, i, s, self)
            ss.__getattribute__(test_name)()

    def test_types(self):
        self.kiddos('test_types')

    def test_values(self):
        self.kiddos('test_values')


class Question:

    type_classes = {'multipleChoice': MultipleChoiceDetails,
                    'matrixChoice': MatrixChoiceDetails,
                    'autoList': AutoListDetails,
                    'manySliders': ManySlidersDetails,
                    'slider': SliderDetails,
                    'starRating': StarRatingDetails}

    def __init__(self, tc, i, loaded, parent):
        # The test case
        self.tc = tc

        # Error message suffix
        self.name_err = 'question definition #{} in '.format(i) \
            + parent.name_err

        # Fill members
        self.name = tc.checkIn(self, loaded, 'name')
        self.type = tc.checkIn(self, loaded, 'type')
        self.details = tc.checkIn(self, loaded, 'details')

    def kiddos(self, test_name):
        details = self.type_classes[self.type](self.tc, self.details, self)
        details.__getattribute__(test_name)()

    def test_types(self):
        self.tc.checkInstance(self, 'name', str)
        self.tc.checkInstance(self, 'type', str)
        self.tc.checkInstance(self, 'details', dict)
        self.kiddos('test_types')

    def test_values(self):
        self.tc.checkInList(self, self.type_classes.keys(), self.type, 'type')
        self.kiddos('test_values')


class bcolors:

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def strip_stacktrace(trace):
    trace = trace[trace.index('\n'):]
    trace = trace[trace.index('\n'):]
    trace = trace[trace.index('\n'):]
    return trace[trace.index(':') + 2:].rstrip('\n')


def green(s):
    return bcolors.OKGREEN + s + bcolors.ENDC


def red(s):
    return bcolors.FAIL + s + bcolors.ENDC


def blue(s):
    return bcolors.OKBLUE + s + bcolors.ENDC


if __name__ == '__main__':
    # Make sure we have a single argument
    if len(sys.argv) != 2:
        sys.exit('Usage: {} file-to-validate'.format(
            os.path.split(sys.argv[0])[1]))
    filename = sys.argv[1]
    basefilename = os.path.split(filename)[1]
    # Don't pass on the argument to unittest
    sys.argv = sys.argv[:1]

    # Our test cases and encouragements
    test_cases = [JSONTestCase, TypesTestCase, ValuesTestCase]
                  #, RootTestCase, FirstLaunchTestCase,
                  #TipiQuestionnaireTestCase, TipiSubQuestionsTestCase,
                  #QuestionsTestCase, QuestionDetailsTestCase,
                  #SubQuestionsTestCase, ConsistencyTestCase]
    ok_texts = ['Yep!', 'Ok!', 'Great!', 'Brilliant!', 'Fantastic!',
                'Perfect!', 'Good!', 'Right you are!', 'Well done!']
    shuffle(ok_texts)

    # Error flag
    error = False

    # Say hello
    hello = "Validating '{}' against grammar version 2.1".format(basefilename)
    print()
    print(hello)
    print("-" * len(hello))
    print()

    for tc, ok in zip(test_cases, ok_texts):
        sys.stdout.write(tc.description + " ... ")
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(tc)
        res = unittest.TestResult()
        suite.run(res)
        if len(res.errors) or len(res.failures):
            error = True
            sys.stdout.write(red('Arg, wrong') + '\r\n')
            print()
            sys.stdout.write(blue("Here's all the information "
                                  "I've got for you:") + '\r\n')

            for k, e in enumerate(res.errors):
                print()
                print("Error #{}".format(k + 1))
                print("--------")
                pprint(e)

            for k, f in enumerate(res.failures):
                print()
                print("Failure #{}".format(k + 1))
                print("----------")
                print(strip_stacktrace(f[1]))

            break
        else:
            sys.stdout.write(green(ok) + '\r\n')

    print()
    if error:
        sys.stdout.write(red("*** Well, there was an error.") + '\r\n')
        sys.stdout.write(red("*** It happens. Try again :-)") + '\r\n')
        sys.exit(1)
    else:
        sys.stdout.write(green("*** You're good to go!") + '\r\n')
        sys.exit(0)
