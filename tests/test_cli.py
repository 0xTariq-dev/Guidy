#!/usr/bin/python3
"""
Contains the class TestcliDocs
"""

import Cli
import inspect
import pep8
import unittest
GuidyAdmin = Cli.GuidyAdmin


class TestcliDocs(unittest.TestCase):
    """Class for testing documentation of the cli"""
    def test_pep8_conformance_cli(self):
        """Test that cli.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['Cli.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_cli_module_docstring(self):
        """Test for the cli.py module docstring"""
        self.assertIsNot(Cli.__doc__, None,
                         "cli.py needs a docstring")
        self.assertTrue(len(Cli.__doc__) >= 1,
                        "cli.py needs a docstring")

    def test_GuidyAdmin_class_docstring(self):
        """Test for the GuidyAdmin class docstring"""
        self.assertIsNot(GuidyAdmin.__doc__, None,
                         "GuidyAdmin class needs a docstring")
        self.assertTrue(len(GuidyAdmin.__doc__) >= 1,
                        "GuidyAdmin class needs a docstring")
