# zenoss-dynamic-inventory

This script will allow you to use Zenoss as an inventory source in Ansible. It organizes your inventory using the last 
portion of your Zenoss group paths (e.g. if your group path is /MYNETWORK/ROUTERS/, your group name is ROUTERS) 
which can then be used when executing an ansible playbook using the --limit argument.


## Usage
1. Place the zenoss-dynamic-inventory.py file in a folder in your ansible project, e.g. ./zenoss-dynamic-inventory/zenoss-dynamic-inventory.py
2. Edit config.ini.example to include your instance name and user account info and rename it to config.ini
3. Install the zenoss python library using ***pip install zenoss***

Usage example: ansible-playbook -i zenoss-dynamic-inventory my-playbook.yml --limit "ROUTERS"

The above command would run the playbook "my-playbook.yml" for all the devices in the "ROUTERS" group of your Zenoss 
instance.


    
    
## License
This project is published with the <a href="https://opensource.org/licenses/MIT" target="_blank">MIT license</a>, so feel free to use the code in your own projects.