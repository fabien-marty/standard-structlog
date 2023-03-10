from __future__ import annotations

import datetime
import json
import logging

import pytest

from stlog.base import STLOG_EXTRA_KEY
from stlog.formatter import (
    DEFAULT_STLOG_DATE_FORMAT,
    DEFAULT_STLOG_HUMAN_FORMAT,
    HumanFormatter,
    JsonFormatter,
)


@pytest.fixture
def log_record() -> logging.LogRecord:
    return logging.LogRecord(
        name="name",
        level=logging.INFO,
        pathname="/foo.py",
        lineno=1,
        msg="foo %s bar %s",
        args=("foo", "bar"),
        exc_info=None,
        func=None,
        sinfo=None,
    )


@pytest.fixture
def human_formatter() -> logging.Formatter:
    return HumanFormatter(
        fmt=DEFAULT_STLOG_HUMAN_FORMAT, datefmt=DEFAULT_STLOG_DATE_FORMAT
    )


@pytest.fixture
def json_formatter() -> logging.Formatter:
    return JsonFormatter()


def test_human1(log_record, human_formatter):
    res = human_formatter.format(log_record)
    assert res.startswith(str(datetime.datetime.utcnow().year))
    assert "[INFO]" in res
    assert "name" in res
    assert "foo foo bar bar" in res


def test_human2(log_record, human_formatter):
    setattr(log_record, STLOG_EXTRA_KEY, ("key1", "key2"))
    log_record.key1 = "value1"
    log_record.key2 = 123
    res = human_formatter.format(log_record)
    assert "[key1: value1]" in res
    assert "[key2: 123]" in res


def test_json1(log_record, json_formatter):
    res = json.loads(json_formatter.format(log_record))
    assert res["logger"]["name"] == log_record.name
    assert res["source"]["path"] == log_record.pathname
    assert res["source"]["lineno"] == log_record.lineno
    assert res["status"] == "info"
    assert res["timestamp"].startswith(str(datetime.datetime.utcnow().year))
    assert res["message"] == "foo foo bar bar"
