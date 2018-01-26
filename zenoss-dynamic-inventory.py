#!/usr/bin/env python
__author__ = 'joshs@nyu.edu'
from zenoss import Zenoss
import json
import argparse
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('config.ini')
uri = parser.get('zenoss', 'uri')
username = parser.get('zenoss', 'username')
password = parser.get('zenoss', 'password')

zenoss = Zenoss(uri, username, password)

class ZenossInventory(object):

    def __init__(self):
        self.inventory = {}
        self.read_cli_args()

        if self.args.list:
            self.inventory = self.get_inventory()
        else:
            # return nothing if --list isn't specified
            self.inventory = self.empty_inventory()

        print json.dumps(self.inventory);

    def empty_inventory(self):
        return {'_meta': {'hostvars': {}}}

    def get_inventory(self):

        hostvars = {}
        groups = {}

        for device in zenoss.get_devices()['devices']:
            if device['groups'] is not None:
                try:
                    for group in device['groups']:
                        group_name = group['name'].split("/")[-1]
                        if group_name in groups:
                            groups[group_name]['hosts'].append(device['name'])
                        else:
                            groups.update({group_name: {'hosts': [], 'vars': {}}})
                            groups[group_name]['hosts'].append(device['name'])
                except IndexError:
                    continue

            if device['hwModel'] is not None:
                hostvars[device['name']] = {}
                facts = {'device_ip': device['ipAddressString'],
                         'hwModel': device['hwModel']['name'],
                        }
                hostvars[device['name']].update(facts)

        result = groups
        result.update({'_meta': {'hostvars': hostvars}})
        return result

    def read_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action='store_true')
        self.args = parser.parse_args()

if __name__ == '__main__':
    # Get the inventory.
    ZenossInventory()