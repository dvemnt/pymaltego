# coding=utf-8

import unittest
import json

from lxml import etree

from pymaltego import entities, exceptions, messages, transforms


class NodeTests(unittest.TestCase):

    """Testing `entities.Node` object."""

    def test_create(self):
        """Testing create instance."""
        name = 'Test'
        node = entities.Node(name)

        self.assertEqual(node.tag, name)
        self.assertEqual(
            etree.tostring(node).decode('ascii'), '<{}/>'.format(name)
        )

    def test_create__with_value(self):
        """Testing create instance with value."""
        name = 'Test'
        node = entities.Node(name, value=name)

        self.assertEqual(
            etree.tostring(node).decode('ascii'), '<{0}>{0}</{0}>'.format(name)
        )

    def test_create__with_parent(self):
        """Testing create instance with parent."""
        parent_name = 'Parent'
        parent = entities.Node(parent_name)
        name = 'Test'
        node = entities.Node(name, parent=parent)

        self.assertEqual(node.getparent(), parent)


class XMLObjectTests(unittest.TestCase):

    """Testing `entities.XMLObject` object."""

    def test_create(self):
        """Testing create instance."""
        xml_object = entities.XMLObject()

        self.assertIsInstance(xml_object, entities.XMLObject)

    def test_create__with_node(self):
        """Testing create instance with node."""
        node = entities.Node('Test')
        xml_object = entities.XMLObject(node=node)

        self.assertIsInstance(xml_object, entities.XMLObject)

    def test_create__with_wrong_node(self):
        """Testing create instance with wrong node."""
        node = 'Test'

        with self.assertRaises(ValueError):
            entities.XMLObject(node=node)

    def test_method_to_node_not_implemented(self):
        """Testing method raises NotImplementedError."""
        xml_object = entities.XMLObject()

        with self.assertRaises(NotImplementedError):
            xml_object.to_node()

    def test_method_to_xml(self):
        """Testing method to_xml."""
        xml_object = entities.XMLObject()

        with self.assertRaises(NotImplementedError):
            xml_object.to_xml()

    def test_method_to_dict(self):
        """Testing method to_dict."""
        xml_object = entities.XMLObject()

        with self.assertRaises(NotImplementedError):
            xml_object.to_dict()


class LabelTests(unittest.TestCase):

    """Testing `entities.Label` object."""

    def test_create(self):
        """Testing create instance."""
        label = entities.Label()

        self.assertIsInstance(label, entities.Label)

    def test_create__with_name(self):
        """Testing create instance with name."""
        name = 'Test'
        label = entities.Label(name=name)

        self.assertEqual(label.name, name)

    def test_create__with_value(self):
        """Testing create instance with value."""
        value = 'Test'
        label = entities.Label(value=value)

        self.assertEqual(label.value, value)

    def test_create__with_content_type(self):
        """Testing create instance with content type."""
        content_type = 'Test'
        label = entities.Label(content_type=content_type)

        self.assertEqual(label.content_type, content_type)

    def test_create__with_node(self):
        """Testing create instance with node."""
        node = entities.Node('Label')
        label = entities.Label(node=node)

        self.assertIsInstance(label, entities.Label)

    def test_create__with_wrong_node(self):
        """Testing create instance with wrong node."""
        node = entities.Node('Wrong')

        with self.assertRaises(exceptions.MalformedEntityError):
            entities.Label(node=node)

    def test_method_to_node(self):
        """Testing method to_node."""
        name = value = content_type = 'Test'
        node = entities.Label(
            name=name, value=value, content_type=content_type
        ).to_node()

        self.assertEqual(node.attrib['Name'], name)
        self.assertEqual(node.attrib['Type'], content_type)
        self.assertEqual(node.text, value)

    def test_method_to_xml(self):
        """Testing method to_xml."""
        name = value = content_type = 'Test'
        label = entities.Label(
            name=name, value=value, content_type=content_type
        )

        self.assertEqual(
            label.to_xml().decode('ascii'),
            (
                '<Label Name="{0}" Type="{0}">'
                '<![CDATA[{0}]]></Label>'
            ).format(name)
        )


class FieldTests(unittest.TestCase):

    """Testing `entities.Field` object."""

    def test_create(self):
        """Testing create instance."""
        field = entities.Field()

        self.assertIsInstance(field, entities.Field)

    def test_create__with_name(self):
        """Testing create instance with name."""
        name = 'Test'
        field = entities.Field(name=name)

        self.assertEqual(field.name, name)

    def test_create__with_value(self):
        """Testing create instance with value."""
        value = 'Test'
        field = entities.Field(value=value)

        self.assertEqual(field.value, value)

    def test_create__with_display_name(self):
        """Testing create instance with display name."""
        display_name = 'Test'
        field = entities.Field(display_name=display_name)

        self.assertEqual(field.display_name, display_name)

    def test_create__with_matching_rule(self):
        """Testing create instance with matching_rule."""
        matching_rule = 'Test'
        field = entities.Field(matching_rule=matching_rule)

        self.assertEqual(field.matching_rule, matching_rule)

    def test_create__with_node(self):
        """Testing create instance with node."""
        node = entities.Node('Field')
        field = entities.Field(node=node)

        self.assertIsInstance(field, entities.Field)

    def test_create__with_wrong_node(self):
        """Testing create instance with wrong node."""
        node = entities.Node('Wrong')

        with self.assertRaises(exceptions.MalformedEntityError):
            entities.Field(node=node)

    def test_method_to_node(self):
        """Testing method to_node."""
        name = value = display_name = matching_rule = 'Test'
        node = entities.Field(
            name=name, value=value, display_name=display_name,
            matching_rule=matching_rule
        ).to_node()

        self.assertEqual(node.attrib['Name'], name)
        self.assertEqual(node.attrib['DisplayName'], display_name)
        self.assertEqual(node.attrib['MatchingRule'], matching_rule)
        self.assertEqual(node.text, value)

    def test_method_to_xml(self):
        """Testing method to_xml."""
        name = value = display_name = matching_rule = 'Test'
        field = entities.Field(
            name=name, value=value, display_name=display_name,
            matching_rule=matching_rule
        )

        self.assertEqual(
            field.to_xml().decode('ascii'),
            (
                '<Field Name="{0}" DisplayName="{0}" MatchingRule="{0}">'
                '{0}</Field>'
            ).format(name)
        )


class EntityTests(unittest.TestCase):

    """Testing `entities.Entity` object."""

    def test_create(self):
        """Testing create instance."""
        entity = entities.Entity()

        self.assertIsInstance(entity, entities.Entity)

    def test_create__with_name(self):
        """Testing create instance with name."""
        name = 'Test'
        entity = entities.Entity(name=name)

        self.assertEqual(entity.name, name)

    def test_create__with_value(self):
        """Testing create instance with value."""
        value = 'Test'
        entity = entities.Entity(value=value)

        self.assertEqual(entity.value, value)

    def test_create__with_weight(self):
        """Testing create instance with weight."""
        weight = 'Test'
        entity = entities.Entity(weight=weight)

        self.assertEqual(entity.weight, weight)

    def test_create__with_icon_url(self):
        """Testing create instance with icon_url."""
        icon_url = 'Test'
        entity = entities.Entity(icon_url=icon_url)

        self.assertEqual(entity.icon_url, icon_url)

    def test_create__with_labels(self):
        """Testing create instance with labels."""
        labels = {'Test': 'Test'}
        entity = entities.Entity(labels=labels)

        self.assertEqual(entity.labels, labels)

    def test_create__with_fields(self):
        """Testing create instance with fields."""
        fields = {'Test': 'Test'}
        entity = entities.Entity(fields=fields)

        self.assertEqual(entity.fields, fields)

    def test_create__with_node(self):
        """Testing create instance with node."""
        node = entities.Node('Entity', attrib={'Type': 'Test'})
        entities.Node('Value', parent=node)
        entity = entities.Entity(node=node)

        self.assertIsInstance(entity, entities.Entity)

    def test_create__with_wrong_node(self):
        """Testing create instance with wrong node."""
        node = entities.Node('Wrong')

        with self.assertRaises(exceptions.MalformedEntityError):
            entities.Entity(node=node)

    def test_create__with_wrong_node_without_type(self):
        """Testing create instance with wrong node without type."""
        node = entities.Node('Entity')

        with self.assertRaises(exceptions.MalformedEntityError):
            entities.Entity(node=node)

    def test_create__with_wrong_node_without_value(self):
        """Testing create instance with wrong node without value."""
        node = entities.Node('Entity', attrib={'Type': 'Test'})

        with self.assertRaises(exceptions.MalformedEntityError):
            entities.Entity(node=node)

    def test_create__with_node_weight(self):
        """Testing create instance with node weight."""
        weight = '0'
        node = entities.Node('Entity', attrib={'Type': 'Test'})
        entities.Node('Value', parent=node)
        entities.Node('Weight', value=weight, parent=node)
        entity = entities.Entity(node=node)

        self.assertEqual(entity.weight, weight)

    def test_create__with_node_additional_fields(self):
        """Testing create instance with node additional fields."""
        field_name = 'Test'
        node = entities.Node('Entity', attrib={'Type': 'Test'})
        entities.Node('Value', parent=node)

        fields = entities.Node('AdditionalFields', parent=node)
        entities.Node('Field', attrib={'Name': field_name}, parent=fields)
        entity = entities.Entity(node=node)

        self.assertIn(field_name, entity.fields)

    def test_create__with_node_labels(self):
        """Testing create instance with node labels."""
        label_name = 'Test'
        node = entities.Node('Entity', attrib={'Type': 'Test'})
        entities.Node('Value', parent=node)

        labels = entities.Node('DisplayInformation', parent=node)
        entities.Node('Label', attrib={'Name': label_name}, parent=labels)
        entity = entities.Entity(node=node)

        self.assertIn(label_name, entity.fields)

    def test_create__with_node_icon_url(self):
        """Testing create instance with node icon url."""
        value = 'Test'
        node = entities.Node('Entity', attrib={'Type': 'Test'})
        entities.Node('Value', parent=node)

        entities.Node('IconURL', value=value, parent=node)
        entity = entities.Entity(node=node)

        self.assertEqual(entity.icon_url, value)

    def test_method_to_node(self):
        """Testing method to_node."""
        name = value = weight = icon_url = 'Test'
        field = entities.Field(value=value)
        label = entities.Label(value=value)
        node = entities.Entity(
            name=name, value=value, weight=weight,
            icon_url=icon_url, fields={'Field': field}, labels={'Label': label}
        ).to_node()

        self.assertEqual(node.attrib['Type'], name)
        self.assertEqual(node.find('Weight').text, weight)
        self.assertEqual(node.find('IconURL').text, icon_url)
        self.assertEqual(node.find('Value').text, value)
        self.assertIn(
            field.value, node.find('AdditionalFields').getchildren()[0].text
        )
        self.assertIn(
            label.value, node.find('DisplayInformation').getchildren()[0].text
        )

    def test_method_to_dict(self):
        """Testing method to_dict."""
        name = value = weight = icon_url = 'Test'
        field = entities.Field(value=value)
        label = entities.Label(value=value)
        d = entities.Entity(
            name=name, value=value, weight=weight,
            icon_url=icon_url, fields={'Field': field}, labels={'Label': label}
        ).to_dict()

        self.assertIn(name, d)
        self.assertIn('fields', d[name])
        self.assertIn('Field', d[name]['fields'])
        self.assertEqual(d[name]['fields']['Field'], value)

    def test_method_to_json(self):
        """Testing method to_dict."""
        name = value = weight = icon_url = 'Test'
        field = entities.Field(value=value)
        label = entities.Label(value=value)
        json_string = entities.Entity(
            name=name, value=value, weight=weight,
            icon_url=icon_url, fields={'Field': field}, labels={'Label': label}
        ).to_json()

        d = json.loads(json_string)

        self.assertIn(name, d)
        self.assertIn('fields', d[name])
        self.assertIn('Field', d[name]['fields'])
        self.assertEqual(d[name]['fields']['Field'], value)

    def test_method_to_json__pretty_print(self):
        """Testing method to_dict."""
        name = value = weight = icon_url = 'Test'
        field = entities.Field(value=value)
        label = entities.Label(value=value)
        json_string = entities.Entity(
            name=name, value=value, weight=weight,
            icon_url=icon_url, fields={'Field': field}, labels={'Label': label}
        ).to_json(pretty_print=True)

        d = json.loads(json_string)

        self.assertIn(name, d)
        self.assertIn('fields', d[name])
        self.assertIn('Field', d[name]['fields'])
        self.assertEqual(d[name]['fields']['Field'], value)


class TransformRequestTests(unittest.TestCase):

    """Testing `messages.TransformRequest`."""

    def test_create(self):
        """Testing create instance."""
        node = entities.Node('MaltegoMessage')
        request = entities.Node('MaltegoTransformRequestMessage', parent=node)
        entities_node = entities.Node('Entities', parent=request)
        entity = entities.Node(
            'Entity', attrib={'Type': 'Test'}, parent=entities_node
        )
        entities.Node('Value', value='Test', parent=entity)

        message = messages.TransformRequest(node=node)

        self.assertIsInstance(message, messages.TransformRequest)

    def test_create__with_node_fields(self):
        """Testing create instance with node fields."""
        node = entities.Node('MaltegoMessage')
        request = entities.Node('MaltegoTransformRequestMessage', parent=node)
        entities_node = entities.Node('Entities', parent=request)
        entity = entities.Node(
            'Entity', attrib={'Type': 'Test'}, parent=entities_node
        )
        entities.Node('Value', value='Test', parent=entity)
        fields = entities.Node('TransformFields', parent=request)
        entities.Node('Field', attrib={'Name': 'Test'}, parent=fields)

        message = messages.TransformRequest(node=node)

        self.assertIsInstance(message, messages.TransformRequest)

    def test_create__with_node_limits(self):
        """Testing create instance with node limits."""
        node = entities.Node('MaltegoMessage')
        request = entities.Node('MaltegoTransformRequestMessage', parent=node)
        entities_node = entities.Node('Entities', parent=request)
        entity = entities.Node(
            'Entity', attrib={'Type': 'Test'}, parent=entities_node
        )
        entities.Node('Value', value='Test', parent=entity)
        entities.Node('Limits', parent=request)

        message = messages.TransformRequest(node=node)

        self.assertIsInstance(message, messages.TransformRequest)

    def test_create__with_wrong_node(self):
        """Testing create instance with wrong node."""
        node = entities.Node('MaltegoMessage')
        entities.Node('MaltegoWrongMessage', parent=node)

        with self.assertRaises(exceptions.MalformedMessageError):
            messages.TransformRequest(node=node)

    def test_create__with_wrong_node_without_entities(self):
        """Testing create instance with wrong node without entities."""
        node = entities.Node('MaltegoMessage')
        entities.Node('MaltegoTransformRequestMessage', parent=node)

        with self.assertRaises(exceptions.MalformedMessageError):
            messages.TransformRequest(node=node)

    def test_create__with_wrong_node_without_field_name(self):
        """Testing create instance with wrong node without field name."""
        node = entities.Node('MaltegoMessage')
        request = entities.Node('MaltegoTransformRequestMessage', parent=node)
        entities_node = entities.Node('Entities', parent=request)
        entity = entities.Node(
            'Entity', attrib={'Type': 'Test'}, parent=entities_node
        )
        entities.Node('Value', value='Test', parent=entity)
        fields = entities.Node('TransformFields', parent=request)
        entities.Node('Field', parent=fields)

        with self.assertRaises(exceptions.MalformedMessageError):
            messages.TransformRequest(node=node)


class TransformResponseTests(unittest.TestCase):

    """Testing `messages.TransformResponse` object."""

    def test_create(self):
        """Testing create instance with entities."""
        entities = ['Entity']
        response = messages.TransformResponse(entities)

        self.assertEqual(response.entities, entities)

    def test_to_node(self):
        """Testing `to_node` method."""
        entity_value = 'Test'
        entity = entities.Entity(name='Test', value=entity_value, labels=None)
        node = messages.TransformResponse([entity]).to_node()

        self.assertEqual(
            entity.value,
            node.find('Entities').getchildren()[0].find('Value').text
        )

    def test_to_node_with_ui_messages(self):
        """Testing `to_node` method with ui messages."""
        entity_value = 'Test'
        ui_messages = {'Key': ['Value']}
        entity = entities.Entity(name='Test', value=entity_value, labels=None)
        node = messages.TransformResponse(
            [entity], ui_messages
        ).to_node()

        self.assertEqual(
            ui_messages['Key'][0],
            node.find('UIMessages').getchildren()[0].text
        )

    def test_method_to_dict(self):
        """Testing method to_dict."""
        entity = entities.Entity(
            name='Test', value='Test', labels={}, fields={}
        )
        d = messages.TransformResponse([entity]).to_dict()

        self.assertIn('entities', d)
        self.assertEqual(d['entities'], [entity.to_dict()])

    def test_to_xml(self):
        """Testing to_xml method."""
        entity = entities.Entity(
            name='Test', value='Test', labels={}, fields={}
        )
        response = messages.TransformResponse([entity])

        needle_xml = (
            '<MaltegoMessage><MaltegoTransformResponseMessage>'
            '<Entities><Entity Type="{}">'
            '<Value>{}</Value></Entity></Entities>'
            '</MaltegoTransformResponseMessage></MaltegoMessage>'
        ).format(entity.name, entity.value)

        self.assertEqual(response.to_xml().decode('ascii'), needle_xml)


class BaseTransformTests(unittest.TestCase):

    """Testsing `transforms.BaseTransform`."""

    def test_create(self):
        """Testing create instance."""
        node = entities.Node('MaltegoMessage')
        request = entities.Node('MaltegoTransformRequestMessage', parent=node)
        entities_node = entities.Node('Entities', parent=request)
        entity = entities.Node(
            'Entity', attrib={'Type': 'Test'}, parent=entities_node
        )
        entities.Node('Value', value='Test', parent=entity)

        message = messages.TransformRequest(node=node)
        transform = transforms.BaseTransform(message)

        self.assertIsInstance(transform, transforms.BaseTransform)

    def test_create__wrong_message(self):
        """Testing create instance with wrong message."""

        with self.assertRaises(ValueError):
            transforms.BaseTransform('wrong')

    def test_method_transform__not_implemented(self):
        """Testing call not implemented method transform."""
        node = entities.Node('MaltegoMessage')
        request = entities.Node('MaltegoTransformRequestMessage', parent=node)
        entities_node = entities.Node('Entities', parent=request)
        entity = entities.Node(
            'Entity', attrib={'Type': 'Test'}, parent=entities_node
        )
        entities.Node('Value', value='Test', parent=entity)

        message = messages.TransformRequest(node=node)
        transform = transforms.BaseTransform(message)

        with self.assertRaises(NotImplementedError):
            transform.transform()

    def test_method_to_response(self):
        """Testing call not implemented method transform."""
        node = entities.Node('MaltegoMessage')
        request = entities.Node('MaltegoTransformRequestMessage', parent=node)
        entities_node = entities.Node('Entities', parent=request)
        entity = entities.Node(
            'Entity', attrib={'Type': 'Test'}, parent=entities_node
        )
        entities.Node('Value', value='Test', parent=entity)

        message = messages.TransformRequest(node=node)
        transform = transforms.BaseTransform(message)

        with self.assertRaises(NotImplementedError):
            transform.to_response()

if __name__ == '__main__':
    unittest.main()
