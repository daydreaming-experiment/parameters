#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Test a parameters file to check it follows grammar v1."""


import json
import unittest
import os
import sys


class ParametersFileTestCase(unittest.TestCase):

    def setUp(self):
        self.f = open(filename, 'r')

    def tearDown(self):
        self.f.close()


class LoadedParametersTestCase(ParametersFileTestCase):

    type_names = {int: 'an integer',
                  float: 'a float',
                  str: 'a string',
                  dict: 'a JSON object',
                  list: 'a list'}
    error_in = "{0} has no '{1}' property"
    error_instance = "'{1}' (in {0}) is not {2}"

    def setUp(self):
        super(LoadedParametersTestCase, self).setUp()
        self.params = json.load(self.f)

    def _test_presence_and_type(self, container, container_name,
                                attr_name, attr_type):
        error_msg = self.error_in.format(container_name, attr_name)
        self.assertIn(attr_name, container, error_msg)
        error_msg = self.error_instance.format(container_name, attr_name,
                                               self.type_names[attr_type])
        self.assertIsInstance(container[attr_name], attr_type, error_msg)


class JSONTestCase(ParametersFileTestCase):

    def test_is_json(self):
        try:
            json.load(self.f)
        except ValueError:
            raise Exception('{} is not valid JSON!'.format(filename))


class RootTestCase(LoadedParametersTestCase):

    def test_is_dict(self):
        self.assertIsInstance(self.params, dict,
                              'Root of the file is not a JSON object')

    def test_version(self):
        self._test_presence_and_type(self.params, 'root object',
                                     'version', int)

    def test_nSlotsPerPoll(self):
        self._test_presence_and_type(self.params, 'root object',
                                     'nSlotsPerPoll', int)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('Usage: {} file-to-validate'.format(
            os.path.split(sys.argv[0])[1]))
    filename = sys.argv[1]
    sys.argv = sys.argv[:1]
    unittest.main()
