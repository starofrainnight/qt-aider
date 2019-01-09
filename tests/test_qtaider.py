#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `qt-aider` package."""

import pytest

from click.testing import CliRunner

from qtaider import qtaider
from qtaider.__main__ import main


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
