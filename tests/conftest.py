"""Pytest configuration and fixtures."""

import os

import pytest


@pytest.fixture(autouse=True)
def reset_cwd():
    """每个测试后重置工作目录"""
    original_cwd = os.getcwd()
    yield
    os.chdir(original_cwd)
