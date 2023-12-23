import json
import os
import random
import time
import uuid


def generate_data(schema, file_count, data_lines, path_to_save, file_name, file_prefix, multiprocessing):
    os.makedirs(path_to_save, exist_ok=True)
    if isinstance(schema, str):
        schema = json.loads(schema)

    for i in range(file_count):
        complete_file_name = f"{file_name}_{file_prefix}{i}.json" if file_prefix else f"{file_name}{i}.json"
        file_path = os.path.join(path_to_save, complete_file_name)
        # result = []
        with open(file_path, 'w') as file:
            for _ in range(data_lines):
                data_entry = generate_data_entry(schema)
                # result.append(data_entry)
                json.dump(data_entry, file)
                file.write('\n')
            # json.dump(result, file)
    print(f"Generated {file_count} files in {path_to_save}.")


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
                options = eval(type_spec)
                data_entry[key] = random.choice(options)

        elif data_type == 'int':
            if type_spec == 'rand':
                data_entry[key] = random.randint(0, 10000)
            elif type_spec.startswith('rand('):
                start, end = map(int, type_spec[5:-1].split(','))
                data_entry[key] = random.randint(start, end)
            elif type_spec.startswith('['):
                options = eval(type_spec)
                data_entry[key] = random.choice(options)

    return data_entry


test_schema = {
        "date": "timestamp:",
        "name": "str:rand",
        "type": "str:['client', 'partner', 'government']",
        "age": "int:rand(1,90)"
    }





