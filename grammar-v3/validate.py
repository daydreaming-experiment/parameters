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

    def setUp(self):
        super(LoadedTestCase, self).setUp()
        self.params = json.load(self.f)

    def checkInstance(self, obj, attr_name, tipe, optional=False):
        if not optional or obj.__getattribute__(attr_name) is not None:
            err = self.error_type.format(obj.name_err, attr_name,
                                         self.type_names[tipe])
            attr = obj.__getattribute__(attr_name)
            self.assertIsInstance(attr, tipe, err)

    def checkInstanceDirectly(self, obj, attr, attr_name, tipe, optional=False):
        if not optional or attr is not None:
            err = self.error_type.format(obj.name_err, attr_name,
                                         self.type_names[tipe])
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

    def checkNotEmpty(self, obj, attr_name):
        err = self.error_empty_list.format(obj.name_err, attr_name)
        attr = obj.__getattribute__(attr_name)
        self.assertTrue(len(attr) > 0, err)

    def checkRegex(self, obj, attr_name, regex, regex_err):
        err = self.error_type.format(obj.name_err, attr_name, regex_err)
        attr = obj.__getattribute__(attr_name)
        self.assertRegexpMatches(attr, regex, err)


class KeysTestCase(LoadedTestCase):

    description = ('Checking all the parameters defined '
                   'are allowed parameters')

    def test_keys(self):
        parameters = Parameters(self, self.params)
        parameters.test_keys()


class TypesTestCase(LoadedTestCase):

    description = ('Checking all the attributes are present '
                   'and have the right types')

    def test_types(self):
        parameters = Parameters(self, self.params)
        parameters.test_types()


class ValuesTestCase(LoadedTestCase):

    description = 'Checking all the values are correct and consistent'

    def test_values(self):
        parameters = Parameters(self, self.params)
        parameters.test_values()


class FixedKeysObject:

    def test_keys(self):
        if isinstance(self.loaded, dict):
            for key in self.loaded.keys():
                msg = key + ' is not an allowed parameter'
                self.tc.checkTrue(self, key in self.authorized_keys, msg)
        kiddos = getattr(self, 'kiddos', None)
        if kiddos is not None:
            kiddos('test_keys')


class Parameters(FixedKeysObject):

    authorized_keys = ['version', 'backendExpId', 'backendDbName',
                       'expDuration', 'backendApiUrl', 'resultsPageUrl',
                       'schedulingMinDelay', 'schedulingMeanDelay',
                       'questions', 'sequences', 'glossary']

    def __init__(self, tc, loaded):
        # The test case
        self.tc = tc
        self.loaded = loaded

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
        self.glossary = tc.checkIn(self, loaded, 'glossary')

    def kiddos(self, test_name):
        for i, q in enumerate(self.questions):
            qq = Question(self.tc, i, q, self)
            qq.__getattribute__(test_name)()

        for i, s in enumerate(self.sequences):
            ss = Sequence(self.tc, i, s, self)
            ss.__getattribute__(test_name)()

        g = Glossary(self.tc, self.glossary, self)
        g.__getattribute__(test_name)()

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
        self.tc.checkInstance(self, 'glossary', dict)
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
                          'schedulingMeanDelay should be at least 5 minutes')
        self.tc.checkRegex(self, 'backendApiUrl', r'^https?://.*[^/]$',
                           'a properly formed url with no trailing slash')
        self.tc.checkRegex(self, 'resultsPageUrl', r'^https?://.*[^/]$',
                           'a properly formed url with no trailing slash')
        self.tc.checkNotEmpty(self, 'questions')
        self.tc.checkNotEmpty(self, 'sequences')
        # question names unique
        names = [q['name'] for q in self.questions]
        numbers = [names.count(n) for n in names]
        self.tc.checkTrue(self, max(numbers) == min(numbers) == 1,
                          'question names must be unique')
        # Number of sequences of each type
        probes = [s for s in self.sequences if s['type'] == 'probe']
        self.tc.checkTrue(self, len(probes) == 1,
                          'there must be exactly one sequence of type probe')
        morningQs = [s for s in self.sequences
                     if s['type'] == 'morningQuestionnaire']
        self.tc.checkTrue(self, len(morningQs) == 1,
                          'there must be exactly one sequence of type '
                          'morningQuestionnaire')
        eveningQs = [s for s in self.sequences
                     if s['type'] == 'eveningQuestionnaire']
        self.tc.checkTrue(self, len(eveningQs) == 1,
                          'there must be exactly one sequence of type '
                          'eveningQuestionnaire')
        beginEndQs = [s for s in self.sequences
                      if s['type'] == 'beginEndQuestionnaire']
        self.tc.checkTrue(self, len(beginEndQs) >= 1,
                          'there must be at least one sequence of type '
                          'beginEndQuestionnaire')
        # sequence names unique
        names = [s['name'] for s in self.sequences]
        numbers = [names.count(n) for n in names]
        self.tc.checkTrue(self, max(numbers) == min(numbers) == 1,
                          'sequence names must be unique')
        self.kiddos('test_values')


# Not a fixed keys object
class Glossary:

    def __init__(self, tc, loaded, parent):
        # The test case
        self.tc = tc
        self.loaded = loaded

        # Error message suffix
        self.name_err = 'glossary in ' + parent.name_err

        self.terms = loaded

    def test_types(self):
        for k, v in self.terms.items():
            self.tc.checkInstanceDirectly(self, k, 'key ' + k, str)
            self.tc.checkInstanceDirectly(self, v, 'value ' + v, str)

    def test_values(self):
        pass

    def test_keys(self):
        pass


class Choice(FixedKeysObject):

    def __init__(self, tc, i, loaded, parent):
        # The test case
        self.tc = tc
        self.loaded = loaded

        # Error message suffix
        self.name_err = 'choice #{} in '.format(i) + parent.name_err

        # Fill members
        self.string = loaded

    def test_types(self):
        self.tc.checkInstance(self, 'string', str)


class MatrixChoice(FixedKeysObject):

    possible_choices = {'Home', 'Commuting', 'Outside',
                        'Public place', 'Work'}

    def __init__(self, tc, i, loaded, parent):
        # The test case
        self.tc = tc
        self.loaded = loaded

        # Error message suffix
        self.name_err = 'choice #{} in '.format(i) + parent.name_err

        # Fill members
        self.string = loaded

    def test_types(self):
        self.tc.checkInstance(self, 'string', str)

    def test_values(self):
        self.tc.checkInList(self, self.possible_choices, self.string,
                            'this matrix choice')


class Hint(FixedKeysObject):

    def __init__(self, tc, i, loaded, parent):
        # The test case
        self.tc = tc
        self.loaded = loaded

        # Error message suffix
        self.name_err = 'hint #{} in '.format(i) + parent.name_err

        # Fill members
        self.string = loaded

    def test_types(self):
        self.tc.checkInstance(self, 'string', str)

    def test_values(self):
        # Nothing to test
        pass


class Slider(FixedKeysObject):

    def __init__(self, tc, i, loaded, parent):
        # The test case
        self.tc = tc
        self.loaded = loaded

        # Error message suffix
        self.name_err = 'slider #{} in '.format(i) + parent.name_err

        # Fill members
        self.string = loaded

    def test_types(self):
        self.tc.checkInstance(self, 'string', str)

    def test_values(self):
        self.tc.checkTrue(self, self.string.count('|') <= 1,
                          'there must be at most one "|"')


class Possibility(FixedKeysObject):

    def __init__(self, tc, i, loaded, parent):
        # The test case
        self.tc = tc
        self.loaded = loaded

        # Error message suffix
        self.name_err = 'possibility #{} in '.format(i) + parent.name_err

        # Fill members
        self.string = loaded

    def test_types(self):
        self.tc.checkInstance(self, 'string', str)

    def test_values(self):
        self.tc.checkTrue(self, self.string.count('|') <= 1,
                          'there must be at most one "|"')


class MultipleChoiceDetails(FixedKeysObject):

    authorized_keys = ['text', 'choices']

    def __init__(self, tc, loaded, parent):
        # The test case
        self.tc = tc
        self.loaded = loaded

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


class MatrixChoiceDetails(FixedKeysObject):

    authorized_keys = ['text', 'choices']

    def __init__(self, tc, loaded, parent):
        # The test case
        self.tc = tc
        self.loaded = loaded

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


class AutoListDetails(FixedKeysObject):

    authorized_keys = ['text', 'hint', 'possibilities']

    def __init__(self, tc, loaded, parent):
        # The test case
        self.tc = tc
        self.loaded = loaded

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


class ManySlidersDetails(FixedKeysObject):

    authorized_keys = ['text', 'availableSliders', 'defaultSliders',
                       'hints', 'addItemHint', 'dialogText',
                       'showLiveIndication', 'initialPosition']

    def __init__(self, tc, loaded, parent):
        # The test case
        self.tc = tc
        self.loaded = loaded

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
        if self.initialPosition is not None:
            self.tc.checkTrue(self, 0 <= self.initialPosition <= 100,
                              'initialPosition must be between 0 and 100')
        for ds in self.defaultSliders:
            self.tc.checkInList(self, self.availableSliders, ds,
                                'this defaultSlider', 'availableSliders')
        self.kiddos('test_values')


class SliderSubQuestion(FixedKeysObject):

    authorized_keys = ['text', 'hints', 'notApplyAllowed',
                       'showLiveIndication', 'initialPosition']

    def __init__(self, tc, i, loaded, parent):
        # The test case
        self.tc = tc
        self.loaded = loaded

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
        if self.initialPosition is not None:
            self.tc.checkTrue(self, 0 <= self.initialPosition <= 100,
                              'initialPosition must be between 0 and 100')
        # No kiddos


class SliderDetails(FixedKeysObject):

    authorized_keys = ['subQuestions']

    def __init__(self, tc, loaded, parent):
        # The test case
        self.tc = tc
        self.loaded = loaded

        # Error message suffix
        self.name_err = 'sliderDetails in ' + parent.name_err

        # Fill members
        self.subQuestions = tc.checkIn(self, loaded, 'subQuestions')

    def kiddos(self, test_name):
        for i, s in enumerate(self.subQuestions):
            ss = SliderSubQuestion(self.tc, i, s, self)
            ss.__getattribute__(test_name)()

    def test_types(self):
        self.tc.checkInstance(self, 'subQuestions', list)
        self.kiddos('test_types')

    def test_values(self):
        self.tc.checkNotEmpty(self, 'subQuestions')
        self.kiddos('test_values')


class StarRatingSubQuestion(FixedKeysObject):

    authorized_keys = ['text', 'hints', 'notApplyAllowed',
                       'showLiveIndication', 'numStars', 'stepSize',
                       'initialRating']

    def __init__(self, tc, i, loaded, parent):
        # The test case
        self.tc = tc
        self.loaded = loaded

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
        if self.initialRating is not None and self.numStars is not None:
            self.tc.checkTrue(self, 0 <= self.initialRating <= self.numStars,
                              'initialRating must be between 0 and numStars')
        if self.numStars is not None:
            self.tc.checkTrue(self, 0 < self.numStars,
                              'numStars must be positive')
        if self.stepSize is not None:
            self.tc.checkTrue(self, 0 < self.stepSize,
                              'stepSize must be positive')
        # No kiddos


class StarRatingDetails(FixedKeysObject):

    authorized_keys = ['subQuestions']

    def __init__(self, tc, loaded, parent):
        # The test case
        self.tc = tc
        self.loaded = loaded

        # Error message suffix
        self.name_err = 'starRatingDetails in ' + parent.name_err

        # Fill members
        self.subQuestions = tc.checkIn(self, loaded, 'subQuestions')

    def kiddos(self, test_name):
        for i, s in enumerate(self.subQuestions):
            ss = StarRatingSubQuestion(self.tc, i, s, self)
            ss.__getattribute__(test_name)()

    def test_types(self):
        self.tc.checkInstance(self, 'subQuestions', list)
        self.kiddos('test_types')

    def test_values(self):
        self.tc.checkNotEmpty(self, 'subQuestions')
        self.kiddos('test_values')


class Question(FixedKeysObject):

    authorized_keys = ['name', 'type', 'details']

    type_classes = {'multipleChoice': MultipleChoiceDetails,
                    'matrixChoice': MatrixChoiceDetails,
                    'autoList': AutoListDetails,
                    'manySliders': ManySlidersDetails,
                    'slider': SliderDetails,
                    'starRating': StarRatingDetails}

    def __init__(self, tc, i, loaded, parent):
        # The test case
        self.tc = tc
        self.loaded = loaded

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


class Sequence(FixedKeysObject):

    authorized_keys = ['name', 'type', 'intro', 'nSlots', 'pageGroups']

    available_types = {'probe', 'beginEndQuestionnaire',
                       'morningQuestionnaire', 'eveningQuestionnaire'}

    def __init__(self, tc, i, loaded, parent):
        # The test case
        self.tc = tc
        self.loaded = loaded
        self.root = parent
        self.parent = parent

        # Error message suffix
        self.name_err = 'sequence definition #{} in '.format(i) \
            + parent.name_err

        # Fill members
        self.name = tc.checkIn(self, loaded, 'name')
        self.type = tc.checkIn(self, loaded, 'type')
        self.intro = tc.checkIn(self, loaded, 'intro')
        self.nSlots = tc.checkIn(self, loaded, 'nSlots')
        self.pageGroups = tc.checkIn(self, loaded, 'pageGroups')

    def kiddos(self, test_name):
        for i, p in enumerate(self.pageGroups):
            pp = PageGroup(self.tc, i, p, self)
            pp.__getattribute__(test_name)()

    def test_types(self):
        self.tc.checkInstance(self, 'name', str)
        self.tc.checkInstance(self, 'type', str)
        self.tc.checkInstance(self, 'intro', str)
        self.tc.checkInstance(self, 'nSlots', int)
        self.tc.checkInstance(self, 'pageGroups', list)
        self.kiddos('test_types')

    def test_values(self):
        self.tc.checkNotEmpty(self, 'pageGroups')
        self.tc.checkInList(self, self.available_types, self.type,
                            'type', 'available types')
        # Values of type
        if self.type == 'probe':
            self.tc.checkTrue(self, self.type == self.name,
                              'for a probe, name must equal type (=probe)')
        if self.type == 'morningQuestionnaire':
            self.tc.checkTrue(self, self.type == self.name,
                              'for an morningQuestionnaire, name must equal '
                              'type (=morningQuestionnaire)')
        if self.type == 'eveningQuestionnaire':
            self.tc.checkTrue(self, self.type == self.name,
                              'for an eveningQuestionnaire, name must equal '
                              'type (=eveningQuestionnaire)')
        # pageGroup names unique
        names = [p['name'] for p in self.pageGroups]
        numbers = [names.count(n) for n in names]
        self.tc.checkTrue(self, max(numbers) == min(numbers) == 1,
                          'pageGroup names must be unique')
        # nSlots is more than fixed positions
        fixeds = {p['position']['fixed'] % self.nSlots for p in self.pageGroups
                  if 'fixed' in p['position']}
        self.tc.checkTrue(self, self.nSlots >= len(fixeds),
                          'nSlots must be >= number of fixed positions')
        floats = {p['position']['floating'] for p in self.pageGroups
                  if 'floating' in p['position']}
        self.tc.checkTrue(self, self.nSlots <= len(fixeds) + len(floats),
                          'nSlots must be <= number of fixed positions + '
                          'number floats')
        if len(floats) > 0:
            self.tc.checkTrue(self, self.nSlots > len(fixeds),
                              'you defined floatings that will never appear '
                              'because nSlots is too small')
        # No defining a position once positive once negative
        positiveFixeds = [p['position']['fixed'] for p in self.pageGroups
                          if 'fixed' in p['position']
                          and p['position']['fixed'] >= 0]
        wrappedNegatives = [p['position']['fixed'] % self.nSlots
                            for p in self.pageGroups
                            if 'fixed' in p['position']
                            and p['position']['fixed'] < 0]
        for w in wrappedNegatives:
            self.tc.checkTrue(self, w not in positiveFixeds,
                              "can't define a fixed position once negative "
                              "once positive")

        self.kiddos('test_values')


class PageGroup(FixedKeysObject):

    authorized_keys = ['name', 'friendlyName', 'position', 'nSlots', 'pages']

    def __init__(self, tc, i, loaded, parent):
        # The test case
        self.tc = tc
        self.loaded = loaded
        self.root = parent.root
        self.parent = parent

        # Error message suffix
        self.name_err = 'pageGroup definition #{} in '.format(i) \
            + parent.name_err

        # Fill members
        self.name = tc.checkIn(self, loaded, 'name')
        self.friendlyName = tc.checkIn(self, loaded, 'friendlyName')
        self.position = tc.checkIn(self, loaded, 'position')
        self.nSlots = tc.checkIn(self, loaded, 'nSlots')
        self.pages = tc.checkIn(self, loaded, 'pages')

    def kiddos(self, test_name):
        p = Position(self.tc, self.position, self)
        p.__getattribute__(test_name)()
        for i, p in enumerate(self.pages):
            pp = Page(self.tc, i, p, self)
            pp.__getattribute__(test_name)()

    def test_types(self):
        self.tc.checkInstance(self, 'name', str)
        self.tc.checkInstance(self, 'friendlyName', str)
        self.tc.checkInstance(self, 'position', dict)
        self.tc.checkInstance(self, 'nSlots', int)
        self.tc.checkInstance(self, 'pages', list)
        self.kiddos('test_types')

    def test_values(self):
        self.tc.checkNotEmpty(self, 'pages')
        # pages names unique
        names = [p['name'] for p in self.pages]
        numbers = [names.count(n) for n in names]
        self.tc.checkTrue(self, max(numbers) == min(numbers) == 1,
                          'page names must be unique')
        # nSlots is more than fixed positions
        fixeds = {p['position']['fixed'] % self.nSlots for p in self.pages
                  if 'fixed' in p['position']}
        self.tc.checkTrue(self, self.nSlots >= len(fixeds),
                          'nSlots must be >= number of fixed positions')
        floats = {p['position']['floating'] for p in self.pages
                  if 'floating' in p['position']}
        self.tc.checkTrue(self, self.nSlots <= len(fixeds) + len(floats),
                          'nSlots must be <= number of fixed positions + '
                          'number floats')
        if len(floats) > 0:
            self.tc.checkTrue(self, self.nSlots > len(fixeds),
                              'you defined floatings that will never appear '
                              'because nSlots is too small')
        # No defining a position once positive once negative
        positiveFixeds = [p['position']['fixed'] for p in self.pages
                          if 'fixed' in p['position']
                          and p['position']['fixed'] >= 0]
        wrappedNegatives = [p['position']['fixed'] % self.nSlots
                            for p in self.pages
                            if 'fixed' in p['position']
                            and p['position']['fixed'] < 0]
        for w in wrappedNegatives:
            self.tc.checkTrue(self, w not in positiveFixeds,
                              "can't define a fixed position once negative "
                              "once positive")
        # Bonus stuff
        bonus = self.position.get('bonus', False)
        if bonus:
            # No bonus page insde a bonus pageGroup
            for p in self.pages:
                self.tc.checkTrue(
                    self, p['position'].get('bonus', False) is False,
                    "can't have a bonus page inside a bonus pageGroup")
        else:
            # Not all bonus quesitons inside a non bonus
            nonbonuses = [p['position'].get('bonus', False) is False
                          for p in self.pages]
            self.tc.checkTrue(self, sum(nonbonuses), "can't have all "
                              "bonus pages in a non-bonus pageGroup")
        # kiddos
        self.kiddos('test_values')


class Page(FixedKeysObject):

    authorized_keys = ['name', 'position', 'nSlots', 'questions']

    def __init__(self, tc, i, loaded, parent):
        # The test case
        self.tc = tc
        self.loaded = loaded
        self.root = parent.root
        self.parent = parent

        # Error message suffix
        self.name_err = 'page definition #{} in '.format(i) \
            + parent.name_err

        # Fill members
        self.name = tc.checkIn(self, loaded, 'name')
        self.position = tc.checkIn(self, loaded, 'position')
        self.nSlots = tc.checkIn(self, loaded, 'nSlots')
        self.questions = tc.checkIn(self, loaded, 'questions')

    def kiddos(self, test_name):
        p = Position(self.tc, self.position, self)
        p.__getattribute__(test_name)()
        for i, q in enumerate(self.questions):
            qq = QuestionReference(self.tc, i, q, self)
            qq.__getattribute__(test_name)()

    def test_types(self):
        self.tc.checkInstance(self, 'name', str)
        self.tc.checkInstance(self, 'position', dict)
        self.tc.checkInstance(self, 'nSlots', int)
        self.tc.checkInstance(self, 'questions', list)
        self.kiddos('test_types')

    def test_values(self):
        self.tc.checkNotEmpty(self, 'questions')
        # question reference names unique
        names = [q['name'] for q in self.questions]
        numbers = [names.count(n) for n in names]
        self.tc.checkTrue(self, max(numbers) == min(numbers) == 1,
                          'question reference names must be unique')
        # nSlots is more than fixed positions
        fixeds = {q['position']['fixed'] % self.nSlots for q in self.questions
                  if 'fixed' in q['position']}
        self.tc.checkTrue(self, self.nSlots >= len(fixeds),
                          'nSlots must be >= number of fixed positions')
        floats = {q['position']['floating'] for q in self.questions
                  if 'floating' in q['position']}
        self.tc.checkTrue(self, self.nSlots <= len(fixeds) + len(floats),
                          'nSlots must be <= number of fixed positions + '
                          'number floats')
        if len(floats) > 0:
            self.tc.checkTrue(self, self.nSlots > len(fixeds),
                              'you defined floatings that will never appear '
                              'because nSlots is too small')
        # No defining a position once positive once negative
        positiveFixeds = [q['position']['fixed'] for q in self.questions
                          if 'fixed' in q['position']
                          and q['position']['fixed'] >= 0]
        wrappedNegatives = [q['position']['fixed'] % self.nSlots
                            for q in self.questions
                            if 'fixed' in q['position']
                            and q['position']['fixed'] < 0]
        for w in wrappedNegatives:
            self.tc.checkTrue(self, w not in positiveFixeds,
                              "can't define a fixed position once negative "
                              "once positive")

        self.kiddos('test_values')


class QuestionReference(FixedKeysObject):

    authorized_keys = ['name', 'questionName', 'position']

    def __init__(self, tc, i, loaded, parent):
        # The test case
        self.tc = tc
        self.loaded = loaded
        self.root = parent.root
        self.parent = parent

        # Error message suffix
        self.name_err = 'questionReference definition #{} in '.format(i) \
            + parent.name_err

        # Fill members
        self.name = tc.checkIn(self, loaded, 'name')
        self.questionName = tc.checkIn(self, loaded, 'questionName')
        self.position = tc.checkIn(self, loaded, 'position')

    def kiddos(self, test_name):
        p = Position(self.tc, self.position, self)
        p.__getattribute__(test_name)()

    def test_types(self):
        self.tc.checkInstance(self, 'name', str)
        self.tc.checkInstance(self, 'questionName', str)
        self.tc.checkInstance(self, 'position', dict)
        self.kiddos('test_types')

    def test_values(self):
        # Reference exists
        qnames = [q['name'] for q in self.root.questions]
        self.tc.checkInList(self, qnames, self.questionName,
                            'question reference', 'question names')
        # After references an existing item
        if 'after' in self.position:
            rnames = [r['name'] for r in self.parent.questions]
            self.tc.checkInList(self, rnames, self.position['after'],
                                'after position', 'question reference names')
            self.tc.checkTrue(self, self.name != self.position['after'],
                              "a question reference can't reference itself "
                              "with an after position")
        # Question can't be bonus
        self.tc.checkTrue(self, self.position.get('bonus', False) is False,
                          'a question cannot be bonus')

        self.kiddos('test_values')


class Position(FixedKeysObject):

    authorized_keys = ['fixed', 'floating', 'after', 'bonus']

    def __init__(self, tc, loaded, parent):
        # The test case
        self.tc = tc
        self.loaded = loaded
        self.root = parent.root
        self.parent = parent

        # Error message suffix
        self.name_err = 'position definition in ' + parent.name_err

        # Fill members
        self.fixed = tc.checkIn(self, loaded, 'fixed', True)
        self.floating = tc.checkIn(self, loaded, 'floating', True)
        self.after = tc.checkIn(self, loaded, 'after', True)
        self.bonus = tc.checkIn(self, loaded, 'bonus', True)

    def test_types(self):
        self.tc.checkInstance(self, 'fixed', int, True)
        self.tc.checkInstance(self, 'floating', str, True)
        self.tc.checkInstance(self, 'after', str, True)
        self.tc.checkInstance(self, 'bonus', bool, True)

    def test_values(self):
        # No wrapping positions
        nSlots = self.parent.parent.nSlots
        if self.fixed is not None:
            self.tc.checkTrue(self, -nSlots <= self.fixed < nSlots,
                              "fixed positions can't double wrap")
        # Only one of fixed, floating, after is defined
        if self.fixed is not None:
            self.tc.checkTrue(self,
                              self.floating is None and self.after is None,
                              'only one of fixed, floating and after '
                              'can be defined')
        if self.floating is not None:
            self.tc.checkTrue(self,
                              self.after is None and self.fixed is None,
                              'only one of fixed, floating and after '
                              'can be defined')
        if self.after is not None:
            self.tc.checkTrue(self,
                              self.fixed is None and self.floating is None,
                              'only one of fixed, floating and after '
                              'can be defined')
        # No kiddos


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
    test_cases = [JSONTestCase, KeysTestCase, TypesTestCase, ValuesTestCase]
    ok_texts = ['Yep!', 'Ok!', 'Great!', 'Brilliant!', 'Fantastic!',
                'Perfect!', 'Good!', 'Right you are!', 'Well done!']
    shuffle(ok_texts)

    # Error flag
    error = False

    # Say hello
    hello = "Validating '{}' against grammar version 3".format(basefilename)
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
