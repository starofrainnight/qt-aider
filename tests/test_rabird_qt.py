#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `rabird.qt` module.
"""

import pytest

from contextlib import contextmanager
from click.testing import CliRunner

import rabird.qt


@pytest.fixture
def response():
    """Sample pytest fixture.
    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    pass


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument.
    """
    pass


def test_command_line_interface():
    pass
