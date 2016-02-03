# Change Log #
All notable changes to this project will be documented in this file.

## [1.0.0] - 2015-11-26 ##
### Added ###
- basic architecture;


## [1.0.1] - 2015-11-27 ##
### Fixed ###
- installation;
- typo in README.md;


## [1.0.2] - 2015-11-27 ##
### Updated ###
- non-required `DisplayName` in `Field`;


## [1.0.3] - 2015-12-01 ##
### Fixed ###
- writing `CDATA`;


## [1.0.4] - 2015-12-19 ##
### Added ###
- simple output entities and response to JSON;

### Updated ###
- empty function docstring;


## [1.0.5] - 2015-12-19 ##
### Added ###
- input request in JSON;


## [1.0.6] - 2015-12-19 ##
### Updated ###
- `transforms.BaseTransform` class takes `message.MaltegoMessage` subclasses;


## [1.0.7] - 2016-01-03 ##
### Fixed ###
- create `entities.Entity` with cached fields and labels;


## [1.1.0] - 2016-01-12 ##
### Added ###
- default `DisplayName` in `entities.Field`;

### Updated ###
- fields as `list` in `entities.Field`;
- labels as `list` in `entities.Field`;
- ui_messages as `list` in `entities.MaltegoMessage`;
- `load_from_node` method as class method `from_node`;
- docstrings;

### Removed ###
- JSON support;


## [1.1.1] - 2016-01-13 ##
### Fixed ###
- `transforms.BaseTransform.to_response`.


## [1.1.2] - 2016-01-22 ##
### Updated ###
- auto create `DisplayName` for fields.


## [1.1.3] - 2016-02-03 ##
### Fixed ###
- docstrings;

### Updated ###
- auto create `DisplayName` for fields.

### Removed ###
- `to_dict` methods;
