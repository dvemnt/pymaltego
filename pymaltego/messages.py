# coding=utf-8

import json

from lxml import etree

from . import entities, exceptions, constants


class MaltegoMessage(entities.XMLObject):

    """Maltego message object."""

    def __init__(self, node=None):
        """
        Initialization object.

        :param node (optional): `etree.Element` instance.
        """
        self.ui_messages = {}
        return super(MaltegoMessage, self).__init__(node)

    def load_from_node(self, node):
        """
        Load values from node.

        :param node: `etree.Element` instance.
        """
        super(MaltegoMessage, self).load_from_node(node)

        node = node.getchildren()[0]

        if node.tag != 'Maltego{}Message'.format(self.__class__.__name__):
            raise exceptions.MalformedMessageError(
                '{} is invalid MaltegoMessage Type.'.format(node.tag)
            )

        return node

    def to_node(self):
        """
        Serialize to `etree.Element` instance.

        :returns: `etree.Element` instance.
        """
        node = entities.Node(
            'Maltego{}Message'.format(self.__class__.__name__)
        )

        if self.ui_messages:
            ui_messages = entities.Node('UIMessages', parent=node)
            for key, value in self.ui_messages.items():
                for message in value:
                    entities.Node(
                        'UIMessage', message, parent=ui_messages,
                        attrib={'MessageType': key}
                    )
        return node

    def to_xml(self, pretty_print=False):
        """
        Serialize to XML string.

        :returns: `str` XML.
        """
        message = entities.Node('MaltegoMessage')
        message.append(self.to_node())
        return etree.tostring(message, pretty_print=pretty_print)

    def to_dict(self):
        """
        Serialize to `dict` instance.

        :returns: `dict` instance.
        """
        return {'entities': [entity.to_dict() for entity in self.entities]}


class JSONTransformRequest(MaltegoMessage):

    """JSON transform request message object."""

    def __init__(self, data=None):
        """
        Initialization object.

        :param data (optional): `str` JSON data.
        """
        self.entities = []
        self.fields = {}
        self.soft_limit = constants.DEFAULT_SOFT_LIMIT
        self.hard_limit = constants.DEFAULT_HARD_LIMIT

        self.load_from_node(data)

    def load_from_node(self, data):
        """
        Load values from data.

        :param node: `str` JSON data.
        """
        try:
            data = json.loads(data)
        except:
            data = [data]

        for value in data:
            self.entities.append(entities.Entity(value=value))


class TransformRequest(MaltegoMessage):

    """Maltego transform request message object."""

    def __init__(self, xml=None, node=None):
        """
        Initialization object.

        :param node (optional): `etree.Element` instance.
        """
        self.entities = []
        self.fields = {}
        self.soft_limit = constants.DEFAULT_SOFT_LIMIT
        self.hard_limit = constants.DEFAULT_HARD_LIMIT

        node = node or etree.fromstring(xml)

        super(TransformRequest, self).__init__(node)

    def load_from_node(self, node):
        """
        Load values from node.

        :param node: `etree.Element` instance.
        """
        node = super(TransformRequest, self).load_from_node(node)

        entity_nodes = node.find('Entities')
        if entity_nodes is None:
            raise exceptions.MalformedMessageError(
                'Request requires "Entities" tag.'
            )

        for entity in entity_nodes.getchildren():
            self.entities.append(entities.Entity(node=entity))

        fields = node.find('TransformFields')
        if fields is not None:
            for field in fields.getchildren():
                if 'Name' not in field.attrib:
                    raise exceptions.MalformedMessageError(
                        'No "Name" attribute in Field'
                    )
                name = field.attrib['Name']
                value = field.text and field.text.strip()
                self.fields[name] = value

        limit = node.find('Limits')
        if limit is not None:
            self.soft_limit = int(
                limit.attrib.get('SoftLimit', constants.DEFAULT_SOFT_LIMIT)
            )
            self.hard_limit = int(
                limit.attrib.get('HardLimit', constants.DEFAULT_SOFT_LIMIT)
            )


class TransformResponse(MaltegoMessage):

    """Maltego transform response message."""

    def __init__(self, entities, ui_messages={}):
        """
        Initialization object.

        :param entities: iterable of `entities.Entity` instances.
        """
        self.ui_messages = ui_messages
        self.entities = list(entities)

    def to_node(self):
        """
        Serialize to `etree.Element` instance.

        :returns: `etree.Element` instance.
        """
        node = super(TransformResponse, self).to_node()

        entities_node = entities.Node('Entities', parent=node)
        for entity in self.entities:
            entities_node.append(entity.to_node())

        return node
