# PyMaltego #
*Package for developing Maltego Transforms*

[![Build Status](https://travis-ci.org/pyvim/pymaltego.svg)](https://travis-ci.org/pyvim/pymaltego)
[![Coverage Status](https://coveralls.io/repos/pyvim/pymaltego/badge.svg?branch=master&service=github)](https://coveralls.io/github/pyvim/pymaltego?branch=master)

## Installation ##

`pip install pymaltego`

## Usage ##

```python
from pymaltego import transforms, messages, entities


class EmailsToUsernamesTransform(transforms.BaseTransform):

    def transform(self):
        usernames = []

        for entity in self.message.entities:
            if len(usernames) >= self.message.soft_limit:
                break

            username = entity.value.split('@')[0]
            usernames.append(entities.Entity(name='Username', value=username))

        return usernames

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
message = messages.TransformRequest(xml=xml)
transform = EmailsToUsernamesTransform(message)
print(transform.to_response().to_xml(pretty_print=True))

<MaltegoMessage>
  <MaltegoTransformResponseMessage>
    <Entities>
      <Entity Type="Username">
        <Value>me</Value>
      </Entity>
    </Entities>
  </MaltegoTransformResponseMessage>
</MaltegoMessage>
```

## Documentation ##
In development. See docstrings.

## Tests ##
```bash
nosetests
```
or
```bash
python tests.py
```

## Changelog ##
See [CHANGELOG.md](https://github.com/pyvim/pymaltego/blob/master/CHANGELOG.md)

## License ##
See [LICENSE](https://github.com/pyvim/pymaltego/blob/master/LICENSE)
