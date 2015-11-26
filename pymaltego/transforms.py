# coding=utf-8

from . import messages


class BaseTransform(object):

    """Base transform object."""

    def __init__(self, message):
        """
        Initialization class.

        :param message: `messages.TransformRequest` instance.
        """
        if not isinstance(message, messages.TransformRequest):
            raise ValueError(
                '`message` must be `messages.TransformRequest` instance.'
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
