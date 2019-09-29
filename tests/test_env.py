import pytest
from unittest.mock import Mock, patch

from tsu.get_shell import GetShell

TERMUX_ID = 100972


class MockPath:
    @staticmethod
    def home():
        return "/data/data/com.termux/files/home"


class TestTodos(object):
    @classmethod
    def setup_class(cls):
        cls.mock_get_patcher = patch("project.services.requests.get")
        cls.mock_get = cls.mock_get_patcher.start()

    @classmethod
    def teardown_class(cls):
        cls.mock_get_patcher.stop()

    def test_new_env(self):
        shell = GetShell(None, 0, 100972).get()
        #
        assert shell == "/system/bin/sh"
