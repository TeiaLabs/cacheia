from cacheia_schemas import Backend

from .templates import (
    create_test_template,
    flush_all_test_template,
    flush_key_test_template,
    flush_some_test_template,
    get_all_test_template,
    get_test_template,
)


def test_create():
    create_test_template(Backend.MEMORY)


def test_get_all():
    get_all_test_template(Backend.MEMORY)


def test_get():
    get_test_template(Backend.MEMORY)


def test_flush_all():
    flush_all_test_template(Backend.MEMORY)


def test_flush_key():
    flush_key_test_template(Backend.MEMORY)


def test_flush_some():
    flush_some_test_template(Backend.MEMORY)


def test_create_with_multiprocessing():
    create_test_template(Backend.MEMORY, True)


def test_get_all_with_multiprocessing():
    get_all_test_template(Backend.MEMORY, True)


def test_get_with_multiprocessing():
    get_test_template(Backend.MEMORY, True)


def test_flush_all_with_multiprocessing():
    flush_all_test_template(Backend.MEMORY, True)


def test_flush_key_with_multiprocessing():
    flush_key_test_template(Backend.MEMORY, True)


def test_flush_some_with_multiprocessing():
    flush_some_test_template(Backend.MEMORY, True)
