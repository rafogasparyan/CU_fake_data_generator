import pytest
from generator.data_generator import generate_data_entry
from generator.data_generator import generate_data
from utils.file_handler import clear_directory  # Adjust import path as needed
import json
import os

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

    # Call the generate_data function using the temporary schema file
    generate_data(temp_schema_file, file_count, data_lines, output_dir, file_name, file_prefix, multiprocessing)

    # Check if the file was created
    generated_file = os.path.join(output_dir, f"{file_name}0.json")
    assert os.path.exists(generated_file), "Data file was not created"


def create_dummy_files(tmp_path, prefix, count):
    for i in range(count):
        file = tmp_path / f"{prefix}{i}.json"
        file.touch()  # Creates an empty file


def test_clear_directory(tmp_path):
    prefix = "test_data_"
    dummy_file_count = 5
    # Create files for the test in the temporary directory
    create_dummy_files(tmp_path, prefix, dummy_file_count)

    # Ensure files are created
    assert len(os.listdir(tmp_path)) == dummy_file_count

    clear_directory(str(tmp_path), prefix)

    # Check if the directory is cleared
    assert len(os.listdir(tmp_path)) == 0, "Directory not cleared properly"

