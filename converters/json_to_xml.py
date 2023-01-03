import json
import os
from lxml import etree as ET

def nested_dict_to_xml(root, d):
    for key, value in d.items():
        if isinstance(value, list):
            for item in value:
                nested_dict_to_xml(ET.SubElement(root, key), item)
        elif isinstance(value, dict):
            nested_dict_to_xml(ET.SubElement(root, key), value)
        else:
            ET.SubElement(root, key).text = str(value)

def get_tree_xml(path, file):
    if file.startswith('stats'):
            return None

    with open(os.path.join(path, file), 'r') as f:
        json_data = json.load(f)

    root = ET.Element('root')
    if not len(json_data) == 0:
        for item in json_data:
            nested_dict_to_xml(ET.SubElement(root, 'item'), item)
        return ET.tostring(root, pretty_print=True)
    else:
        print(f'No data in file: {file}')
        return None