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
            Question(self.tc, self, i, q).test_types()

        #for s in self.sequences:
            #Sequence(tc, self, s).test_types()


class MultipleChoiceDetails:
    pass


class MatrixChoiceDetails:
    pass


class AutoListDetails:
    pass


class ManySlidersDetails:
    pass


class SliderDetails:
    pass


class StarRatingDetails:
    pass


class Question:

    type_classes = {'multipleChoice': MultipleChoiceDetails,
                    'matrixChoice': MatrixChoiceDetails,
                    'autoList': AutoListDetails,
                    'manySliders': ManySlidersDetails,
                    'slider': SliderDetails,
                    'starRating': StarRatingDetails}

    def __init__(self, tc, root, i, loaded):
        # The test case
        self.tc = tc

        # Error message suffix
        self.name_err = 'question definition #{}'.format(i)

        # Fill members
        self.name = tc.checkIn(self, loaded, 'name')
        self.type = tc.checkIn(self, loaded, 'type')
        self.details = tc.checkIn(self, loaded, 'details')

    def test_types(self):
        self.tc.checkInstance(self, 'name', str)
        self.tc.checkInstance(self, 'type', str)
        self.tc.checkInstance(self, 'details', dict)

        details = self.type_classes[self.type]()
        #details.test_types()


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
