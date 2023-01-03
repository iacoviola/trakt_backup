import json
import os
import xml.etree.ElementTree as ET

def nested_dict_to_xml(root, d):
    for key, value in d.items():
        if not isinstance(value, dict):
            ET.SubElement(root, key).text = str(value)
        else:
            nested_dict_to_xml(ET.SubElement(root, key), value)

def get_tree_xml(path, file):
    if file.startswith('stats'):
            return None

    with open(os.path.join(path, file), 'r') as f:
        json_data = json.load(f)

    root = ET.Element('root')
    if not len(json_data) == 0:
        for item in json_data:
            record = ET.SubElement(root, 'record')
            for key, value in item.items():
                if not isinstance(value, dict):
                    ET.SubElement(record, key).text = str(value)
                else:
                    nested_dict_to_xml(ET.SubElement(record, key), value)
        return ET.ElementTree(root)
    else:
        print(f'No data in file: {file}')
        return None