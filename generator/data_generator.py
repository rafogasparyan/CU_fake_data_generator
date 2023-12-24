import random
import time
import uuid
from multiprocessing import Pool
import os
import json
import logging




def generate_data_entry(schema):
    data_entry = {}
    for key, value_type in schema.items():
        data_type, type_spec = value_type.split(':', 1)
        if data_type == 'timestamp':
            data_entry[key] = time.time()
        elif data_type == 'str':
            if type_spec == 'rand':
                data_entry[key] = str(uuid.uuid4())
            elif type_spec.startswith('['):
                json_formatted_spec = type_spec.replace("'", '"')
                options = json.loads(json_formatted_spec)
                data_entry[key] = random.choice(options)
        elif data_type == 'int':
            if type_spec == 'rand':
                data_entry[key] = random.randint(0, 10000)
            elif type_spec.startswith('rand('):
                start, end = map(int, type_spec[5:-1].split(','))
                data_entry[key] = random.randint(start, end)
            elif type_spec.startswith('['):
                options_str = type_spec.replace("'", "\"")
                options = json.loads(options_str)
                data_entry[key] = random.choice(options)
            elif not (type_spec.startswith('rand') or type_spec.startswith('[')):
                logging.error(f"Invalid schema for integer type: {key}:{value_type}")
                data_entry[key] = None

    return data_entry


def generate_single_file(args):
    schema, data_lines, file_path = args
    with open(file_path, 'w') as file:
        for _ in range(data_lines):
            data_entry = generate_data_entry(schema)
            json.dump(data_entry, file)
            file.write('\n')


def generate_data(schema, file_count, data_lines, path_to_save, file_name, file_prefix, multiprocessing):
    os.makedirs(path_to_save, exist_ok=True)
    if os.path.isfile(schema):
        with open(schema, 'r') as schema_file:
            schema = json.load(schema_file)
    elif isinstance(schema, str):
        schema = json.loads(schema)

    # Prepare the arguments for each process
    args_list = []
    for i in range(file_count):
        complete_file_name = f"{file_name}_{file_prefix}{i}.json" if file_prefix else f"{file_name}{i}.json"
        file_path = os.path.join(path_to_save, complete_file_name)
        args_list.append((schema, data_lines, file_path))

    # Use a multiprocessing pool to generate files in parallel
    with Pool(processes=multiprocessing) as pool:
        pool.map(generate_single_file, args_list)

    print(f"Generated {file_count} files in {path_to_save}.")




