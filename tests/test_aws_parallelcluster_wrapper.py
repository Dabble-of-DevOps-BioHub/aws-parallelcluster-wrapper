#!/usr/bin/env python

"""Tests for `aws_parallelcluster_wrapper` package."""


import unittest
from click.testing import CliRunner

from aws_parallelcluster_wrapper import aws_parallelcluster_wrapper
from aws_parallelcluster_wrapper import cli


class TestAws_parallelcluster_wrapper(unittest.TestCase):
    """Tests for `aws_parallelcluster_wrapper` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'aws_parallelcluster_wrapper.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
