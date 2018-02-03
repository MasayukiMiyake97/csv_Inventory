#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
This module reads the CSV file and converts it into inventory information.
"""

import csv
import yaml
import json
import sys

TYPE_STRING  = 'S'
TYPE_INTEGER = 'I'
TYPE_BOOLEAN = 'B'
TYPE_FLOAT   = 'F'

def load_csv_inventory(file_name):
    """
    Read inventory file in CSV format.

    :param string file_name: csv file name
    :rtype: array
    :return: node information array.
    """ 

    # load csv
    ret = []

    with open(file_name, 'r') as csv_file:
        reader = csv.reader(csv_file, dialect='excel')
        # load header
        header = next(reader)
        header_info = load_header(header)
        # load node information
        for row in reader:
            if len(row) <= 0:
                continue

            node_info = load_node_info(header_info, row)
            ret.append(node_info)

    return ret


def load_header(header):
    """
    Read header line.
    Returns an array of header information.
    header information format => [{"item_type": Type, "item_name": item name},...]
    ex. [{"item_type": "S", "item_name": "ansible_host"}, ...]

    :param array header: Element array of headers.
    :rtype: array
    :return: Array of header information.
    """ 

    ret = []

    for item in header:
        item = item.strip()
        elements = item.split('.')
        if len(elements) >= 2:
            item_type = elements[0].strip()
            item_name = elements[1].strip()
            ret.append({'item_type': item_type, 'item_name': item_name})
        else:
            ret = None
            break

    return ret


def load_node_info(header_info_array, item_array):
    """
    Read node information line.
    Returns an dict of node information.
    node information format => {item_name1: value1, item_name2: value2, ...}
    ex. {"host_name": "web001", "port_no": 80, ... }

    :param array header_info_array: Array of .
    :param array item_array: Array of node information.
    :rtype: dict
    :return: Dict of node information.
    """ 

    ret = {}

    pos = 0
    for header in header_info_array:
        item = item_array[pos].strip()
        item_type = header['item_type']
        item_name = header['item_name']

        val = conv_str2value(item_type, item)
        if val is not None:
            ret[item_name] = val

        pos += 1

    return ret


def load_common_info(file_name):
    """
    Read node information line.
    Returns an dict of node information.
    node information format => {item_name1: value1, item_name2: value2, ...}
    ex. {"host_name": "web001", "port_no": 80, ... }

    :param string file_name: Name of common definition file in yaml format.
    :rtype: dict
    :return: Dict of common information.
    """ 

    ret = None
    with open(file_name, 'r') as common_file:
        ret = yaml.load(common_file)

    return ret


def conv_str2value(item_type, item):
    """
    Convert a character string to a specified data type.

    :param string item_type: A character string representing the type of item data.
    :param string item: Value of item data.
    :rtype: undecided
    :return: The converted value.
    """ 

    ret = None

    if len(item) <= 0:
        return None

    if TYPE_STRING == item_type:
        ret = item
    elif TYPE_INTEGER == item_type:
        ret = int(item)
    elif TYPE_BOOLEAN == item_type:
        item = item.lower()
        if item == 'true':
            ret = True
        elif item == 'false':
            ret = False
        else:
            ret = False
    elif TYPE_FLOAT == item_type:
        ret = float(item)
    else:
        ret = item

    return ret


def make_hostvars(node_info_array):

    ret = {}

    for node_info in node_info_array:
        #" get host_name
        host_name = node_info.pop('host_name', None)
        if host_name is None:
            ret = None
            break
        # make hostvar
        ret[host_name] = node_info

    return ret


def make_groups(hostvars):

    ret = {}

    for node_name, node_info in hostvars.items():
        # get group name
        group_name = node_info.pop('group', None)
        if group_name is None:
            ret = None
            break
        # make groups
        if group_name in ret:
            group = ret[group_name]
            hosts = group['hosts']
            hosts.append(node_name)
        else:
            group = {}
            hosts = []
            hosts.append(node_name)
            group['hosts'] = hosts
            ret[group_name] = group

    return ret


def add_groupvars(groups, common_info):

    # get group_vars
    if 'group_vars' in common_info: 
        group_vars = common_info['group_vars']
        for name, val in group_vars.items():
            if name in groups:
                groups[name]['vars'] = val
    # get all vars
    if 'all_vars' in common_info:
        all_vars = common_info['all_vars']
	groups['all'] = {'vars': all_vars}


def make_specific_items(node_info_array, common_info):

    return node_info_array


def main():

    common_info = load_common_info('common_val.yml')
    node_info_array = load_csv_inventory('inventory.csv') 

    node_info_array = make_specific_items(node_info_array, common_info)

    hostvars = make_hostvars(node_info_array)
    groups = make_groups(hostvars)

    add_groupvars(groups, common_info)

    groups['_meta'] = {'hostvars': hostvars}

    json.dump(groups, sys.stdout)

 
if __name__ == '__main__':

    main()

