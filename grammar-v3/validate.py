#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Test a parameters file to check it follows grammar v3."""


import json
import unittest
import os
#import re
import sys
#from functools import partial
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
    error_list_type = "'{1}' (in {0}) contains items that are not {2}"
    error_empty_list = "'{1}' (in {0}) is an empty list"
    warn_default = "You defined '{1}' (in {0}) but set it to its default value"

    def setUp(self):
        super(LoadedTestCase, self).setUp()
        self.params = json.load(self.f)

    def checkInstance(self, obj, attr_name, tipe):
        err = self.error_type.format(obj.name_err, attr_name,
                                     self.type_names[tipe])
        attr = obj.__getattribute__(attr_name)
        self.assertIsInstance(attr, tipe, err)

    def checkIn(self, obj, container, attr_name):
        err = self.error_in.format(obj.name_err, attr_name)
        self.assertIn(attr_name, container, err)
        return container[attr_name]


class TypesTestCase(LoadedTestCase):

    description = ('Checking all the attributes are present '
                   'and have the right types')

    def test_types(self):
        parameters = Parameters(self, self.params)
        parameters.test_types()


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

        for i, q in enumerate(self.questions):
            Question(self.tc, i, q, self).test_types()

        #for s in self.sequences:
            #Sequence(tc, self, s).test_types()


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

    # TODO: test values: there's only one |


class MultipleChoiceDetails:

    def __init__(self, tc, loaded, parent):
        # The test case
        self.tc = tc

        # Error message suffix
        self.name_err = 'multipleChoiceDetails in ' + parent.name_err

        # Fill members
        self.text = tc.checkIn(self, loaded, 'text')
        self.choices = tc.checkIn(self, loaded, 'choices')

    def test_types(self):
        self.tc.checkInstance(self, 'text', str)
        self.tc.checkInstance(self, 'choices', list)
        for i, c in enumerate(self.choices):
            Choice(self.tc, i, c, self).test_types()


class MatrixChoiceDetails:

    def __init__(self, tc, loaded, parent):
        # The test case
        self.tc = tc

        # Error message suffix
        self.name_err = 'matrixChoiceDetails in ' + parent.name_err

        # Fill members
        self.text = tc.checkIn(self, loaded, 'text')
        self.choices = tc.checkIn(self, loaded, 'choices')

    def test_types(self):
        self.tc.checkInstance(self, 'text', str)
        self.tc.checkInstance(self, 'choices', list)
        for i, c in enumerate(self.choices):
            Choice(self.tc, i, c, self).test_types()

    # TODO: test values of 'choices'


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

    def test_types(self):
        self.tc.checkInstance(self, 'text', str)
        self.tc.checkInstance(self, 'hint', str)
        self.tc.checkInstance(self, 'possibilities', list)
        for i, p in enumerate(self.possibilities):
            Possibility(self.tc, i, p, self).test_types()


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
        self.showLiveIndication = loaded.get('showLiveIndication', None)
        self.initialPosition = loaded.get('initialPosition', None)

    def test_types(self):
        self.tc.checkInstance(self, 'text', str)
        self.tc.checkInstance(self, 'availableSliders', list)
        for i, s in enumerate(self.availableSliders):
            Slider(self.tc, i, s, self).test_types()
        self.tc.checkInstance(self, 'defaultSliders', list)
        for i, s in enumerate(self.defaultSliders):
            Slider(self.tc, i, s, self).test_types()
        self.tc.checkInstance(self, 'hints', list)
        for i, h in enumerate(self.hints):
            Hint(self.tc, i, h, self).test_types()
        self.tc.checkInstance(self, 'addItemHint', str)
        self.tc.checkInstance(self, 'dialogText', str)
        if self.showLiveIndication is not None:
            self.tc.checkInstance(self, 'showLiveIndication', bool)
        if self.initialPosition is not None:
            self.tc.checkInstance(self, 'initialPosition', int)

    # TODO: test values. number of hints, defaultSliders in availableSliders.
    # value of initialPosition


class SliderSubQuestion:

    def __init__(self, tc, i, loaded, parent):
        # The test case
        self.tc = tc

        # Error message suffix
        self.name_err = 'subQuestion #{} in '.format(i) + parent.name_err

        # Fill members
        self.text = tc.checkIn(self, loaded, 'text')
        self.hints = tc.checkIn(self, loaded, 'hints')
        self.notApplyAllowed = loaded.get('notApplyAllowed', None)
        self.showLiveIndication = loaded.get('showLiveIndication', None)
        self.initialPosition = loaded.get('initialPosition', None)

    def test_types(self):
        self.tc.checkInstance(self, 'text', str)
        self.tc.checkInstance(self, 'hints', list)
        for i, h in enumerate(self.hints):
            Hint(self.tc, i, h, self).test_types()
        if self.notApplyAllowed is not None:
            self.tc.checkInstance(self, 'notApplyAllowed', bool)
        if self.showLiveIndication is not None:
            self.tc.checkInstance(self, 'showLiveIndication', bool)
        if self.initialPosition is not None:
            self.tc.checkInstance(self, 'initialPosition', int)

    # TODO: test values: at least two hints, value of initialPosition


class SliderDetails:

    def __init__(self, tc, loaded, parent):
        # The test case
        self.tc = tc

        # Error message suffix
        self.name_err = 'sliderDetails in ' + parent.name_err

        # Fill members
        self.subQuestions = tc.checkIn(self, loaded, 'subQuestions')

    def test_types(self):
        for i, s in enumerate(self.subQuestions):
            SliderSubQuestion(self.tc, i, s, self).test_types()


class StarRatingSubQuestion:

    def __init__(self, tc, i, loaded, parent):
        # The test case
        self.tc = tc

        # Error message suffix
        self.name_err = 'subQuestion #{} in '.format(i) + parent.name_err

        # Fill members
        self.text = tc.checkIn(self, loaded, 'text')
        self.hints = tc.checkIn(self, loaded, 'hints')
        self.notApplyAllowed = loaded.get('notApplyAllowed', None)
        self.showLiveIndication = loaded.get('showLiveIndication', None)
        self.numStars = loaded.get('numStars', None)
        self.stepSize = loaded.get('stepSize', None)
        self.initialRating = loaded.get('initialRating', None)

    def test_types(self):
        self.tc.checkInstance(self, 'text', str)
        self.tc.checkInstance(self, 'hints', list)
        for i, h in enumerate(self.hints):
            Hint(self.tc, i, h, self).test_types()
        if self.notApplyAllowed is not None:
            self.tc.checkInstance(self, 'notApplyAllowed', bool)
        if self.showLiveIndication is not None:
            self.tc.checkInstance(self, 'showLiveIndication', bool)
        if self.numStars is not None:
            self.tc.checkInstance(self, 'numStars', int)
        if self.stepSize is not None:
            self.tc.checkInstance(self, 'stepSize', float)
        if self.initialRating is not None:
            self.tc.checkInstance(self, 'initialRating', float)

    # TODO: test values: at least two hints,
    # values of initialRating, numStars, stepSize


class StarRatingDetails:

    def __init__(self, tc, loaded, parent):
        # The test case
        self.tc = tc

        # Error message suffix
        self.name_err = 'starRatingDetails in ' + parent.name_err

        # Fill members
        self.subQuestions = tc.checkIn(self, loaded, 'subQuestions')

    def test_types(self):
        for i, s in enumerate(self.subQuestions):
            StarRatingSubQuestion(self.tc, i, s, self).test_types()


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

    def test_types(self):
        self.tc.checkInstance(self, 'name', str)
        self.tc.checkInstance(self, 'type', str)
        self.tc.checkInstance(self, 'details', dict)

        details = self.type_classes[self.type](self.tc, self.details, self)
        details.test_types()

    # TODO: test values of 'details'


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
    test_cases = [JSONTestCase, TypesTestCase]#, RootTestCase, FirstLaunchTestCase,
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
