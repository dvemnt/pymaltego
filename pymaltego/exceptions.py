# coding=utf-8


class PyMaltegoException(Exception):

    """Base exception class."""

    pass


class MalformedEntityError(PyMaltegoException):
    pass


class MalformedMessageError(PyMaltegoException):
    pass
