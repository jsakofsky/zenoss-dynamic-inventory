#!/usr/bin/env python
__author__ = 'joshs@nyu.edu'
from zenoss import Zenoss
import json
import argparse
from ConfigParser import SafeConfigParser

# get zenoss url/user/pass from config.ini file in local directory
parser = SafeConfigParser()
parser.read('config.ini')
uri = parser.get('zenoss', 'uri')
username = parser.get('zenoss', 'username')
password = parser.get('zenoss', 'password')

# create connection and zenoss obj
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
        # no data for you!!!!
        return {'_meta': {'hostvars': {}}}

    def get_inventory(self):

        hostvars = {}
        groups = {}

        for device in zenoss.get_devices()['devices']:
            # skip if device isn't in at least one group
            if device['groups'] is not None:
                try:
                    for group in device['groups']:
                        # only use the last part of group as group name
                        group_name = group['name'].split("/")[-1]
                        if group_name in groups:
                            # if group already found, just add host to it
                            groups[group_name]['hosts'].append(device['name'])
                        else:
                            # otherwise create group and add host to it
                            groups.update({group_name: {'hosts': [], 'vars': {}}})
                            groups[group_name]['hosts'].append(device['name'])
                except IndexError:
                    continue
            
            # add hwModel info and ip address to facts
            # todo: add more info to facts
            if device['hwModel'] is not None:
                hostvars[device['name']] = {}
                facts = {'device_ip': device['ipAddressString'],
                         'hwModel': device['hwModel']['name'],
                        }
                hostvars[device['name']].update(facts)
        
        # add the facts to the results, just the facts
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
