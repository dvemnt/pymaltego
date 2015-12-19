# coding=utf-8

from . import messages


class BaseTransform(object):

    """Base transform object."""

    def __init__(self, message):
        """
        Initialization class.

        :param message: `messages.MaltegoMessage` subclasses instance.
        """
        if not issubclass(message.__class__, messages.MaltegoMessage):
            raise ValueError(
                'message should be instance of'
                ' `messages.MaltegoMessage` subclass.'
            )
        self.message = message

    def transform(self):
        """
        Do transform.

        :returns: iterable object of `entities.Entity` instances.
        """
        raise NotImplementedError('Object should contains method `transform`.')

    def to_response(self):
        """
        Create `messages.TransformResponse` instance.

        :returns: `messages.TransformResponse` instance.
        """
        return messages.TransformResponse(entities=self.transform())
