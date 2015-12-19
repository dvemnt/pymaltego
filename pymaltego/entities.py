# coding=utf-8

import json

from lxml import etree

from . import exceptions


class Node(object):

    """Node object."""

    def __new__(self, name, value=None, parent=None, **kwargs):
        """
        Create object.

        :param name: name of node.
        :param value (optional): text of node.
        :param parent (optional): `etree.Element` instance parent of node.
        :param kwargs (optional): `dict` of arguments.
        """
        element = etree.Element(name, **kwargs)

        if value is not None:
            element.text = value

        if parent is not None:
            parent.append(element)

        return element


class XMLObject(object):

    """XML object."""

    def __init__(self, node=None):
        """
        Initialization object.

        :param node (optional): `etree.Element` instance.
        """
        if node is not None:
            self.load_from_node(node)

    def load_from_node(self, node):
        """
        Load values from node.

        :param node: `etree.Element` instance.
        """
        if not etree.iselement(node):
            raise ValueError('Is not an `etree.Element` instance.')

    def to_node(self):
        """
        Serialize to `etree.Element` instance.

        :returns: `etree.Element` instance.
        """
        raise NotImplementedError('Object should contains method `to_node`.')

    def to_dict(self):
        """
        Serialize to `dict` instance.

        :returns: `dict` instance.
        """
        raise NotImplementedError('Object should contains method `to_dict`.')

    def to_xml(self, pretty_print=False):
        """
        Serialize to XML string.

        :returns: `str` XML.
        """
        return etree.tostring(self.to_node(), pretty_print=pretty_print)

    def to_json(self, pretty_print=False):
        """
        Serialize to JSON string.

        :returns: `str` JSON.
        """
        if pretty_print:
            return json.dumps(self.to_dict(), sort_keys=True, indent=4)
        return json.dumps(self.to_dict())


class Label(XMLObject):

    """Label object."""

    def __init__(self, name='', value='', content_type='text/html',
                 node=None):
        """
        Initialization object.

        :param name (optional): label name.
        :param value (optional): label value.
        :param content_type (optional): label content type.
        :param node (optional): `etree.Element` instance.
        """
        self.name = name
        self.value = value
        self.content_type = content_type
        return super(Label, self).__init__(node)

    def load_from_node(self, node):
        """
        Load values from node.

        :param node: `etree.Element` instance.
        """
        super(Label, self).load_from_node(node)

        if node.tag != self.__class__.__name__:
            raise exceptions.MalformedEntityError(
                '{} not a "{}" tag.'.format(node.tag, self.__class__.__name__)
            )

        self.name = node.attrib.get('Name', '')
        self.content_type = node.attrib.get('Type', '')
        self.value = node.text and node.text.strip()

    def to_node(self):
        """
        Serialize to `etree.Element` instance.

        :returns: `etree.Element` instance.
        """
        node = Node('Label')
        node.attrib['Name'] = self.name
        node.attrib['Type'] = self.content_type
        node.text = etree.CDATA(self.value)
        return node


class Field(XMLObject):

    """Field object."""

    def __init__(self, name='', value='', display_name='',
                 matching_rule=None, node=None):
        """
        Initialization object.

        :param name (optional): field name.
        :param value (optional): field value.
        :param display_name (optional): field display name.
        :param matching_rule (optional): field matching rule.
        :param node (optional): `etree.Element` instance.
        """
        self.name = name
        self.value = value
        self.display_name = display_name
        self.matching_rule = matching_rule
        super(Field, self).__init__(node)

    def load_from_node(self, node):
        """
        Load values from node.

        :param node: `etree.Element` instance.
        """
        super(Field, self).load_from_node(node)

        if node.tag != self.__class__.__name__:
            raise exceptions.MalformedEntityError(
                '{} not a "{}" tag'.format(node.tag, self.__class__.__name__)
            )

        self.name = node.attrib.get('Name')
        self.value = node.text and node.text.strip()
        self.display_name = node.attrib.get('DisplayName')
        self.matching_rule = node.attrib.get('MatchingRule')

    def to_node(self):
        """
        Serialize to `etree.Element` instance.

        :returns: `etree.Element` instance.
        """
        node = Node('Field', self.value)
        node.attrib['Name'] = self.name

        if self.display_name is not None:
            node.attrib['DisplayName'] = self.display_name

        if self.matching_rule is not None:
            node.attrib['MatchingRule'] = self.matching_rule
        return node


class Entity(XMLObject):

    """Entity base object."""

    def __init__(self, name='', value='', weight=None, icon_url=None,
                 labels={}, fields={}, node=None):
        """
        Initialization object.

        :param name (optional): entity name.
        :param value (optional): entity value.
        :param weight (optional): entity weight.
        :param icon_url (optional): entity icon url.
        :param labels (optional): entity display information.
        :param fields (optional): `dict` of `Field` instance.
        :param node (optional): `etree.Element` instance.
        """
        self.name = name
        self.value = value
        self.weight = weight
        self.icon_url = icon_url
        self.fields = fields
        self.labels = labels

        self.node = node

        super(Entity, self).__init__(node)

    def load_from_node(self, node):
        """
        Load values from node.

        :param node: `etree.Element` instance.
        """
        super(Entity, self).load_from_node(node)

        if node.tag != self.__class__.__name__:
            raise exceptions.MalformedEntityError(
                '{} not a {}.'.format(node.tag, self.__class__.__name__)
            )

        if 'Type' not in node.attrib:
            raise exceptions.MalformedEntityError('No "Type" attribute.')
        self.name = node.attrib['Type']

        value = node.find('Value')
        if value is None:
            raise exceptions.MalformedEntityError('Missing "Value" tag.')
        self.value = value.text and value.text.strip()

        weight = node.find('Weight')
        if weight is not None:
            self.weight = weight.text and weight.text.strip()

        additional_fields = node.find('AdditionalFields')
        if additional_fields is not None:
            for field_node in additional_fields.getchildren():
                field = Field(node=field_node)
                self.fields[field.name] = field

        labels = node.find('DisplayInformation')
        if labels is not None:
            for label_node in labels.getchildren():
                label = Label(node=label_node)
                self.labels[label.name] = label

        icon_url = node.find('IconURL')
        if icon_url is not None:
            self.icon_url = icon_url.text and icon_url.text.strip()

    def to_node(self):
        """
        Serialize to `etree.Element` instance.

        :returns: `etree.Element` instance.
        """
        node = Node('Entity')
        node.attrib['Type'] = self.name

        Node('Value', self.value, parent=node)

        if self.weight is not None:
            Node('Weight', self.weight, parent=node)

        if self.fields:
            additional_fields = Node('AdditionalFields', parent=node)
            for field in self.fields.values():
                if field.value:
                    additional_fields.append(field.to_node())

        if self.labels:
            labels = Node('DisplayInformation', parent=node)
            for label in self.labels.values():
                labels.append(label.to_node())

        if self.icon_url is not None:
            Node('IconURL', value=self.icon_url, parent=node)

        return node

    def to_dict(self):
        """
        Serialize to `dict` instance.

        :returns: `dict` instance.
        """
        result = {}
        result[self.name] = {}
        result[self.name]['value'] = self.value
        result[self.name]['weight'] = self.weight

        result[self.name]['fields'] = {
            key: field.value for key, field in self.fields.items()
        }

        return result
