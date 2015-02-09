#!/usr/bin/python

# zabbix_configuration.py

# Copyright (c) 2015, Gyorgy Szombathelyi. All rights reserved.

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA


DOCUMENTATION = '''

module: zabbix_configuration
short_description: Import Zabbix configurations
description:
    - This module will let you import Zabbix exported configurations from xml or json sources.
author: Gyorgy Szombathelyi
requirements:
    - zabbix-api python module
options:
    server_url:
        description:
            - Url of Zabbix server, with protocol (http or https).
              C(url) is an alias for C(server_url).
        required: true
        default: null
        aliases: [ "url" ]
    login_user:
        description:
            - Zabbix user name.
        required: true
        default: null
    login_password:
        description:
            - Zabbix user password.
        required: true
        default: null
    format:
        description:
            - Format of the import data
        choices: ['xml', 'json']
    filename:
        description:
            - Filename to import from
        required: true
'''

from zabbix_api import ZabbixAPI

def main():
  module = AnsibleModule(
    argument_spec = dict(
      server_url=dict(required=True, default=None, aliases=['url']),
      login_user=dict(required=True, default=None),
      login_password=dict(required=True, default=None),
      format    = dict(default='xml', choices=['xml', 'json']),
      filename  = dict(required=True),
    )
  )

  try:
    zbx = ZabbixAPI(module.params.get('server_url'))
    zbx.login(module.params.get('login_user'), module.params.get('login_password'))
  except BaseException as e:
    module.fail_json(msg="Failed to connect to Zabbix server: %s" % e)

  rules={
    "applications":{
            "createMissing": True,
            "updateExisting": True
           },
    "discoveryRules":{
            "createMissing": True,
            "updateExisting": True
           },
    "graphs":{
            "createMissing": True,
            "updateExisting": True
           },
    "groups":{
            "createMissing": True,
            "updateExisting": True
           },
    "hosts":{
            "createMissing": True,
            "updateExisting": True
           },
    "images":{
            "createMissing": True,
            "updateExisting": True
           },
    "items":{
            "createMissing": True,
            "updateExisting": True
           },
    "maps":{
            "createMissing": True,
            "updateExisting": True
           },
    "screens":{
            "createMissing": True,
            "updateExisting": True
           },
    "templateLinkage":{
            "createMissing": True,
            "updateExisting": True
           },
    "templates":{
            "createMissing": True,
            "updateExisting": True
           },
    "templateScreens":{
            "createMissing": True,
            "updateExisting": True
           },
    "triggers":{
            "createMissing": True,
            "updateExisting": True
           }
       }

  try:
    with open(module.params.get('filename')) as f:
      content=f.read()
      zbx.configuration.import_( {
        'format': module.params.get('format'),
        'rules': rules,
        'source': content
      } )
  except BaseException as e:
    module.fail_json(msg="Failed to import configuration: %s" % e)

  module.exit_json(changed=True)

from ansible.module_utils.basic import *
main()
