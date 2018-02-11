# zenoss-dynamic-inventory

This script will allow you to use Zenoss as an inventory source in Ansible. It organizes your inventory using the last 
portion of your Zenoss group paths (e.g. if your group path is /MYNETWORK/ROUTERS/, your group name is ROUTERS) 
which can then be used when executing an ansible playbook using the --limit argument.



## Usage

**Requirements**
1. Place the zenoss-dynamic-inventory.py file in a folder in your ansible project, e.g. _./zenoss-dynamic-inventory/zenoss-dynamic-inventory.py_
2. Edit config.ini.example to include your instance name and user account info and rename it to config.ini
3. Install the zenoss and requests python libraries using ***pip install zenoss requests***

Usage examples:

**Run on all devices**
```shell
ansible-playbook -i zenoss-dynamic-inventory my-playbook.yml
```
**Run on a specific group named ROUTERS**
```shell
ansible-playbook -i zenoss-dynamic-inventory my-playbook.yml --limit "ROUTERS"
```
**Run on a specific host**
```shell
ansible-playbook -i zenoss-dynamic-inventory my-playbook.yml --limit "hostname-in-zenoss"
```

## Host Variables returned
Currently, this version returns the following host variables:
* hwModel
* device_ip
    
## License
This project is published with the <a href="https://opensource.org/licenses/MIT" target="_blank">MIT license</a>.
