# coding=utf-8

import unittest

from lxml import etree

from pymaltego import entities, exceptions, messages, transforms


class NodeTests(unittest.TestCase):

    """Testing `pymaltego.entities.Node` object."""

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

    def test_create__with_unicode_value(self):
        name = 'Test'
        value = u'\xf3'
        node = entities.Node(name, value=value)

        self.assertTrue(etree.tostring(node))


class XMLObjectTests(unittest.TestCase):

    """Testing `pymaltego.entities.XMLObject` object."""

    def test_create(self):
        """Testing create instance."""
        xml_object = entities.XMLObject()

        self.assertIsInstance(xml_object, entities.XMLObject)

    def test_create__with_wrong_node(self):
        """Testing create instance with wrong node."""
        node = 'Test'

        with self.assertRaises(ValueError):
            entities.XMLObject.from_node(node)

    def test_method_to_node(self):
        """Testing method raises NotImplementedError."""
        xml_object = entities.XMLObject()

        with self.assertRaises(NotImplementedError):
            xml_object.to_node()

    def test_method_to_xml(self):
        """Testing method to_xml."""
        xml_object = entities.XMLObject()

        with self.assertRaises(NotImplementedError):
            xml_object.to_xml()


class LabelTests(unittest.TestCase):

    """Testing `pymaltego.entities.Label` object."""

    def test_create(self):
        """Testing create instance."""
        name = value = 'Test'
        label = entities.Label(name=name, value=value)

        self.assertIsInstance(label, entities.Label)
        self.assertEqual(label.name, name)
        self.assertEqual(label.value, value)

    def test_create__with_content_type(self):
        """Testing create instance with content type."""
        name = value = content_type = 'Test'
        label = entities.Label(
            name=name, value=value, content_type=content_type
        )

        self.assertEqual(label.content_type, content_type)

    def test_create_from_node(self):
        """Testing create instance with node."""
        node = entities.Node('Label', 'Test', attrib={'Name': 'Test'})
        label = entities.Label.from_node(node=node)

        self.assertIsInstance(label, entities.Label)

    def test_create__with_wrong_node(self):
        """Testing create instance with wrong node."""
        node = entities.Node('Wrong')

        with self.assertRaises(exceptions.MalformedEntityError):
            entities.Label.from_node(node=node)

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

    """Testing `pymaltego.entities.Field` object."""

    def test_create(self):
        """Testing create instance with name."""
        name = value = 'Test'
        field = entities.Field(name=name, value=value)

        self.assertEqual(field.name, name)
        self.assertEqual(field.display_name, name)

    def test_create__with_display_name(self):
        """Testing create instance with display name."""
        name = value = display_name = 'Test'
        field = entities.Field(
            name=name, value=value, display_name=display_name
        )

        self.assertEqual(field.display_name, display_name)

    def test_create__with_auto_display_name(self):
        """Testing create instance with display name."""
        name = value = 'test'
        field = entities.Field(name=name, value=value)

        self.assertEqual(field.display_name, 'Test')

    def test_create__with_auto_display_name_multiple(self):
        """Testing create instance with display name."""
        name = value = 'test_case'
        field = entities.Field(name=name, value=value)

        self.assertEqual(field.display_name, 'Test Case')

    def test_create__with_matching_rule(self):
        """Testing create instance with matching_rule."""
        name = value = matching_rule = 'Test'
        field = entities.Field(
            name=name, value=value, matching_rule=matching_rule
        )

        self.assertEqual(field.matching_rule, matching_rule)

    def test_create__with_node(self):
        """Testing create instance with node."""
        node = entities.Node('Field', 'Test', attrib={'Name': 'Test'})
        field = entities.Field.from_node(node=node)

        self.assertIsInstance(field, entities.Field)

    def test_create__with_wrong_node(self):
        """Testing create instance with wrong node."""
        node = entities.Node('Wrong')

        with self.assertRaises(exceptions.MalformedEntityError):
            entities.Field.from_node(node=node)

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

    """Testing `pymaltego.entities.Entity` object."""

    def test_create(self):
        """Testing create instance."""
        name = value = 'Test'
        entity = entities.Entity(name=name, value=value)

        self.assertIsInstance(entity, entities.Entity)
        self.assertEqual(entity.name, name)
        self.assertEqual(entity.value, value)

    def test_create__with_weight(self):
        """Testing create instance with weight."""
        name = value = weight = 'Test'
        entity = entities.Entity(name=name, value=value, weight=weight)

        self.assertEqual(entity.weight, weight)

    def test_create__with_icon_url(self):
        """Testing create instance with icon_url."""
        name = value = icon_url = 'Test'
        entity = entities.Entity(name=name, value=value, icon_url=icon_url)

        self.assertEqual(entity.icon_url, icon_url)

    def test_create__with_labels(self):
        """Testing create instance with labels."""
        name = value = 'Test'
        labels = []
        entity = entities.Entity(name=name, value=value, labels=labels)

        self.assertEqual(entity.labels, labels)

    def test_create__with_fields(self):
        """Testing create instance with fields."""
        name = value = 'Test'
        fields = []
        entity = entities.Entity(name=name, value=value, fields=fields)

        self.assertEqual(entity.fields, fields)

    def test_create__with_node(self):
        """Testing create instance with node."""
        node = entities.Node('Entity', attrib={'Type': 'Test'})
        entities.Node('Value', parent=node)
        entity = entities.Entity.from_node(node=node)

        self.assertIsInstance(entity, entities.Entity)

    def test_create__with_wrong_node(self):
        """Testing create instance with wrong node."""
        node = entities.Node('Wrong')

        with self.assertRaises(exceptions.MalformedEntityError):
            entities.Entity.from_node(node=node)

    def test_create__wrong_node_type(self):
        """Testing create instance with wrong node without type."""
        node = entities.Node('Entity')

        with self.assertRaises(exceptions.MalformedEntityError):
            entities.Entity.from_node(node=node)

    def test_create__wrong_node_value(self):
        """Testing create instance with wrong node without value."""
        node = entities.Node('Entity', attrib={'Type': 'Test'})

        with self.assertRaises(exceptions.MalformedEntityError):
            entities.Entity.from_node(node=node)

    def test_create__node_weight(self):
        """Testing create instance with node weight."""
        weight = '0'
        node = entities.Node('Entity', attrib={'Type': 'Test'})
        entities.Node('Value', parent=node)
        entities.Node('Weight', value=weight, parent=node)
        entity = entities.Entity.from_node(node=node)

        self.assertEqual(entity.weight, weight)

    def test_create__additional_fields(self):
        """Testing create instance with node additional fields."""
        field_name = 'Test'
        node = entities.Node('Entity', attrib={'Type': 'Test'})
        entities.Node('Value', parent=node)

        fields = entities.Node('AdditionalFields', parent=node)
        entities.Node('Field', 'V', attrib={'Name': field_name}, parent=fields)
        entity = entities.Entity.from_node(node=node)

        self.assertEqual(len(entity.fields), 1)

    def test_create__with_node_labels(self):
        """Testing create instance with node labels."""
        label_name = 'Test'
        node = entities.Node('Entity', 'Test', attrib={'Type': 'Test'})
        entities.Node('Value', parent=node)

        labels = entities.Node('DisplayInformation', parent=node)
        entities.Node('Label', 'V', attrib={'Name': label_name}, parent=labels)
        entity = entities.Entity.from_node(node=node)

        self.assertEqual(len(entity.labels), 1)

    def test_create__with_node_icon_url(self):
        """Testing create instance with node icon url."""
        value = 'Test'
        node = entities.Node('Entity', attrib={'Type': 'Test'})
        entities.Node('Value', parent=node)

        entities.Node('IconURL', value=value, parent=node)
        entity = entities.Entity.from_node(node=node)

        self.assertEqual(entity.icon_url, value)

    def test_method_to_node(self):
        """Testing method to_node."""
        name = value = weight = icon_url = 'Test'
        field = entities.Field(name=name, value=value)
        label = entities.Label(name=name, value=value)
        node = entities.Entity(
            name=name, value=value, weight=weight,
            icon_url=icon_url, fields=[field], labels=[label]
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


class TransformRequestTests(unittest.TestCase):

    """Testing `pymaltego.messages.TransformRequest`."""

    def test_create(self):
        """Testing create instance."""
        node = entities.Node('MaltegoMessage')
        request = entities.Node('MaltegoTransformRequestMessage', parent=node)
        entities_node = entities.Node('Entities', parent=request)
        entity = entities.Node(
            'Entity', attrib={'Type': 'Test'}, parent=entities_node
        )
        entities.Node('Value', value='Test', parent=entity)

        message = messages.TransformRequest.from_node(node=node)

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

        message = messages.TransformRequest.from_node(node=node)

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

        message = messages.TransformRequest.from_node(node=node)

        self.assertIsInstance(message, messages.TransformRequest)

    def test_create__with_wrong_node(self):
        """Testing create instance with wrong node."""
        node = 'Test'

        with self.assertRaises(ValueError):
            messages.TransformRequest.from_node(node)

    def test_create__with_wrong_tag(self):
        """Testing create instance with wrong node."""
        node = entities.Node('MaltegoMessage')
        entities.Node('MaltegoWrongMessage', parent=node)

        with self.assertRaises(exceptions.MalformedMessageError):
            messages.TransformRequest.from_node(node=node)

    def test_create__without_entities(self):
        """Testing create instance with wrong node without entities."""
        node = entities.Node('MaltegoMessage')
        entities.Node('MaltegoTransformRequestMessage', parent=node)

        with self.assertRaises(exceptions.MalformedMessageError):
            messages.TransformRequest.from_node(node=node)

    def test_create__without_field_name(self):
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
            messages.TransformRequest.from_node(node=node)

    def test_create_from_xml(self):
        """Testing create instance from XML."""
        xml = '''
            <MaltegoMessage>
              <MaltegoTransformRequestMessage>
                <Entities>
                  <Entity Type="EmailAddress">
                    <Value>me@pyvim.com</Value>
                  </Entity>
                </Entities>
                <Limits SoftLimit="12" HardLimit="12"/>
              </MaltegoTransformRequestMessage>
            </MaltegoMessage>
        '''
        message = messages.TransformRequest.from_xml(xml)

        self.assertEqual(message.entities[0].value, 'me@pyvim.com')


class TransformResponseTests(unittest.TestCase):

    """Testing `pymaltego.messages.TransformResponse` object."""

    def test_create(self):
        """Testing create instance with entities."""
        entities_iter = ['Entity']
        response = messages.TransformResponse(entities_iter)

        self.assertEqual(response.entities, entities_iter)

    def test_from_node(self):
        """Testing create instance from node."""
        node = entities.Node('MaltegoMessage')
        request = entities.Node('MaltegoTransformResponseMessage', parent=node)
        entities_node = entities.Node('Entities', parent=request)
        entity = entities.Node(
            'Entity', 'Test', attrib={'Type': 'Test'}, parent=entities_node
        )
        entities.Node('Value', value='Test', parent=entity)
        ui_messages_node = entities.Node('UIMessages', parent=request)
        entities.Node(
            'UIMessage', 'Test', attrib={'MessageType': 'Test'},
            parent=ui_messages_node
        )

        instance = messages.TransformResponse.from_node(node)

        self.assertIsInstance(instance, messages.TransformResponse)
        self.assertEqual(instance.entities[0].value, 'Test')
        self.assertEqual(instance.ui_messages[0].value, 'Test')

    def test_from_node__without_entities(self):
        """Testing create instance from node."""
        node = entities.Node('MaltegoMessage')
        request = entities.Node('MaltegoTransformResponseMessage', parent=node)
        entities.Node('Entitie', parent=request)

        with self.assertRaises(exceptions.MalformedMessageError):
            messages.TransformResponse.from_node(node)

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
        ui_messages = [entities.UIMessage('Test', 'Test')]
        entity = entities.Entity(name='Test', value=entity_value, labels=None)
        node = messages.TransformResponse(
            [entity], ui_messages
        ).to_node()

        self.assertEqual(
            ui_messages[0].value,
            node.find('UIMessages').getchildren()[0].text
        )

    def test_to_xml(self):
        """Testing to_xml method."""
        entity = entities.Entity(
            name='Test', value='Test'
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

    """Testing `pymaltego.transforms.BaseTransform`."""

    def test_create(self):
        """Testing create instance."""
        node = entities.Node('MaltegoMessage')
        request = entities.Node('MaltegoTransformRequestMessage', parent=node)
        entities_node = entities.Node('Entities', parent=request)
        entity = entities.Node(
            'Entity', attrib={'Type': 'Test'}, parent=entities_node
        )
        entities.Node('Value', value='Test', parent=entity)

        message = messages.TransformRequest.from_node(node=node)
        transform = transforms.BaseTransform(message)

        self.assertIsInstance(transform, transforms.BaseTransform)

    def test_create__wrong_message(self):
        """Testing create instance with wrong message."""

        with self.assertRaises(ValueError):
            transforms.BaseTransform('wrong')

    def test_method_transform(self):
        """Testing call not implemented method transform."""
        node = entities.Node('MaltegoMessage')
        request = entities.Node('MaltegoTransformRequestMessage', parent=node)
        entities_node = entities.Node('Entities', parent=request)
        entity = entities.Node(
            'Entity', attrib={'Type': 'Test'}, parent=entities_node
        )
        entities.Node('Value', value='Test', parent=entity)

        message = messages.TransformRequest.from_node(node=node)
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

        message = messages.TransformRequest.from_node(node=node)
        transform = transforms.BaseTransform(message)

        with self.assertRaises(NotImplementedError):
            transform.to_response()


class UIMessageTests(unittest.TestCase):

    """Testing `pymaltego.entities.UIMessage`."""

    def test_from_node(self):
        """Testing create instance from node."""
        node = entities.Node('UIMessage', 'Test', attrib={'MessageType': 'ts'})
        instance = entities.UIMessage.from_node(node)

        self.assertIsInstance(instance, entities.UIMessage)
        self.assertEqual(instance.value, 'Test')
        self.assertEqual(instance.message_type, 'ts')

    def test_to_xml(self):
        """Testing convert instance to XML."""
        instance = entities.UIMessage('Test', 'Test')

        self.assertEqual(
            instance.to_xml().decode('ascii'),
            '<UIMessage MessageType="Test">Test</UIMessage>'
        )

if __name__ == '__main__':
    unittest.main()
