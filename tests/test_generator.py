import pytest
from generator.data_generator import generate_data_entry
from generator.data_generator import generate_data
from utils.file_handler import clear_directory  # Adjust import path as needed
import json
import os
from generator.schema_parser import parse_schema, validate_schema
import logging

# Test data
test_data_types = [
    ({"date": "timestamp:"}, float),
    ({"name": "str:rand"}, str),
    ({"age": "int:rand"}, int),
    ({"role": "str:['admin', 'user', 'guest']"}, str),
    ({"score": "int:rand(1, 100)"}, int)
]


@pytest.mark.parametrize("schema, expected_type", test_data_types)
def test_generate_data_entry(schema, expected_type):
    data_entry = generate_data_entry(schema)
    for key, value in data_entry.items():
        assert isinstance(value, expected_type), f"Value for {key} is not of expected type {expected_type}"


test_schemas = [
    ({"name": "str:rand"}, ["name"]),
    ({"age": "int:rand"}, ["age"]),
    ({"date": "timestamp:"}, ["date"]),
    ({"role": "str:['admin', 'user', 'guest']"}, ["role"]),
    ({"score": "int:rand(1, 100)"}, ["score"]),
    ({"name": "str:rand", "email": "str:rand", "isActive": "str:['True', 'False']"}, ["name", "email", "isActive"]),
    ({"age": "int:rand", "score": "int:rand(1, 100)", "level": "int:[1, 2, 3, 4, 5]"}, ["age", "score", "level"]),
    ({"timestamp": "timestamp:", "event": "str:['click', 'view', 'exit']", "sessionID": "str:rand"},
     ["timestamp", "event", "sessionID"]),
    ({"product": "str:['Book', 'Laptop', 'Phone']", "quantity": "int:rand(1, 10)", "inStock": "str:['True', 'False']"},
     ["product", "quantity", "inStock"]),
    ({"date": "timestamp:", "temperature": "int:rand(-20, 40)", "humidity": "int:rand(0, 100)"},
     ["date", "temperature", "humidity"])
]


@pytest.mark.parametrize("schema, expected_keys", test_schemas)
def test_different_data_schemas(schema, expected_keys):
    data_entry = generate_data_entry(schema)
    for key in expected_keys:
        assert key in data_entry, f"Expected key '{key}' is missing in the generated data entry"


# Fixture to create a temporary schema file
"""    
The tmp_path fixture creates a temporary directory that is unique to the test run.
All files created during the test (including the schema file and any generated data files) 
are stored in this temporary directory.
After the test finishes (whether it passes or fails), pytest automatically cleans up the temporary directory 
and all its contents.
"""
@pytest.fixture
def temp_schema_file(tmp_path):
    schema = {
        "name": "str:rand",
        "age": "int:rand"
    }
    file = tmp_path / "schema.json"
    with open(file, 'w') as f:
        json.dump(schema, f)
    return str(file)


def test_generate_data_with_schema_file(temp_schema_file):
    file_count = 2
    data_lines = 5
    output_dir = os.path.dirname(temp_schema_file)
    file_name = "test"
    file_prefix = None
    multiprocessing = 1

    generate_data(temp_schema_file, file_count, data_lines, output_dir, file_name, file_prefix, multiprocessing)

    # Check if the file is created
    generated_file = os.path.join(output_dir, f"{file_name}0.json")
    assert os.path.exists(generated_file), "Data file was not created"


def create_dummy_files(tmp_path, prefix, count):
    for i in range(count):
        file = tmp_path / f"{prefix}{i}.json"
        # Creates an empty file
        file.touch()


def test_clear_directory(tmp_path):
    prefix = "test_data_"
    dummy_file_count = 5
    # Create files for the test in the temporary directory
    create_dummy_files(tmp_path, prefix, dummy_file_count)

    # Check if files are created
    assert len(os.listdir(tmp_path)) == dummy_file_count

    clear_directory(str(tmp_path), prefix)

    # Check if the files are deleted
    assert len(os.listdir(tmp_path)) == 0, "Directory not cleared properly"


def test_file_saving_to_disk(tmp_path):
    # Define test parameters for the file that will be created
    file_name = "test_output"
    file_count = 1
    data_lines = 2
    output_dir = tmp_path
    schema = '{"name": "str:rand", "age": "int:rand"}'

    generate_data(schema, file_count, data_lines, str(output_dir), file_name, None, 1)

    # Construct the expected file path
    expected_file_path = output_dir / f"{file_name}0.json"

    # Check if the file is created
    assert os.path.exists(expected_file_path), "Output file was not created"

    # Just in case check the content in the file
    with open(expected_file_path, 'r') as file:
        lines = file.readlines()
        assert len(lines) == data_lines, "Incorrect number of lines in the file"



def test_multiprocessing_file_generation(tmp_path):
    file_name = "test_output"
    file_count = 5
    data_lines = 10
    output_dir = tmp_path
    schema = '{"name": "str:rand", "age": "int:rand"}'
    multiprocessing = 2  # Set to a value greater than 1

    generate_data(schema, file_count, data_lines, str(output_dir), file_name, None, multiprocessing)

    # Check if the correct number of files are created
    generated_files = os.listdir(output_dir)
    assert len(generated_files) == file_count, f"Expected {file_count} files, but found {len(generated_files)}"



def test_invalid_schemas():
    invalid_schemas = [
        '{"name": "int:hello"}',  # Invalid int format
        '{"timestamp": "str:now"}',  # Invalid timestamp format
        '{"age": "str:25"}'  # Type mismatch
    ]

    for schema_str in invalid_schemas:
        schema = parse_schema(schema_str)
        with pytest.raises(ValueError):  # Expect a ValueError to be raised
            validate_schema(schema)


