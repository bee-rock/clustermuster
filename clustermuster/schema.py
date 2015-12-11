from jsonschema import validate


def validate_json(command):
    schema = {"title": "command",
              "type": "object",
              "properties": {
                             "name": {"type": "string"},
                             "command": {"type": "string"},
                             },
              "required": ["name", "command"]
              }
    validate(command, schema)
