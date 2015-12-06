from pycommandcenter.schema import validate_json
import base
from jsonschema import ValidationError
import json


class Test(base.CQSTest):

    def test_json_fits_schema_request(self):
        valid_json = '{"name": "any", "command":"Rossum"}'
        validate_json(json.loads(valid_json))

    def test_json_does_not_fit_scheme(self):
        json_with_bad_schema = '{"first_name": "Guido", "last_name":"Rossum"}'
        self.assertRaises(ValidationError, validate_json, json.loads(json_with_bad_schema))
