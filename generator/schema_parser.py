import json
import os
import re


def parse_schema(schema_str):
    try:
        if os.path.isfile(schema_str):
            with open(schema_str, 'r') as file:
                schema = json.load(file)
        else:
            schema = json.loads(schema_str)
        return schema
    except Exception as e:
        raise ValueError(f"Failed to parse schema: {e}")


def validate_schema(schema):
    valid_types = {'timestamp', 'str', 'int'}
    type_pattern = re.compile(r'^(timestamp|str|int):(.*)$')

    for key, value in schema.items():
        match = type_pattern.match(value)
        if not match:
            raise ValueError(f"Invalid format for key '{key}': '{value}'")

        data_type, type_spec = match.groups()

        if data_type == 'timestamp' and type_spec:
            raise ValueError(f"Timestamp type for key '{key}' should not have a specifier: '{type_spec}'")

        if data_type == 'str':
            if type_spec != 'rand' and not re.match(r"^\[.*\]$", type_spec):
                raise ValueError(f"Invalid specifier for string type '{key}': '{type_spec}'")

        if data_type == 'int':
            if not re.match(r"^(rand(\(\d+,\s*\d+\))?|\[\d+(,\s*\d+)*\])$", type_spec):
                raise ValueError(f"Invalid specifier for int type '{key}': '{type_spec}'")

    return True


# Example usage
example_schema = {
    "date": "timestamp:",
    "name": "str:rand",
    "type": "str:['client', 'partner', 'government']",
    "age": "int:rand(1, 90)"
}
a = json.dumps(example_schema)
print(parse_schema(a))
try:
    is_valid = validate_schema(example_schema)
    print("Schema is valid.")
except ValueError as e:
    print(e)
