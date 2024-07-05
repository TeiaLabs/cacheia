from .templates import (
    create_test_template,
    flush_all_test_template,
    flush_key_test_template,
    flush_some_test_template,
    get_all_test_template,
    get_test_template,
)


def test_create():
    create_test_template("mongo")


def test_get_all():
    get_all_test_template("mongo")


def test_get():
    get_test_template("mongo")


def test_flush_all():
    flush_all_test_template("mongo")


def test_flush_key():
    flush_key_test_template("mongo")


def test_flush_some():
    flush_some_test_template("mongo")
