import pandas
import json
import os

def flatten_json(item, prev_key=None):
    record = dict()
    for key, value in item.items():
        if isinstance(value, list):
            for i, it in enumerate(value):
                item_record = flatten_json(it, f'{key}/{i + 1}')
                for key_nest, value_nest in item_record.items():
                    if prev_key is not None:
                        record[f'{prev_key}_{key}_{i + 1}_{key_nest}'] = value_nest
                    else:
                        record[f'{key}_{key_nest}'] = value_nest
        elif isinstance(value, dict):
            record_nest = flatten_json(value)
            for key_nest, value_nest in record_nest.items():
                record[f'{key}_{key_nest}'] = value_nest
        else:
            record[key] = value
    return record

def get_dataframe_csv(path, file):
    if file.startswith('stats'):
        return None

    with open(os.path.join(path, file), 'r') as f:
        json_data = json.load(f)
        list_new_data = list()

        print(f'{len(json_data)} records in file: {file}')
        if not len(json_data) == 0:
            for item in json_data:
                list_new_data.append(flatten_json(item))
            return pandas.DataFrame(list_new_data)
        else:
            print(f'No data in file: {file}')
            return None