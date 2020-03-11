#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2013, Chatham Financial <oss@chathamfinancial.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}


DOCUMENTATION = '''
---
module: kafka_topics
short_description: Manage topics kafka
description:
  - This module can be used to create, delete or config topics kafka.
version_added: "2.9"
author:
  - Thibault Lecoq

'''

EXAMPLES = '''

'''

RETURN = '''

'''

import os
from ansible.module_utils.basic import AnsibleModule

from confluent_kafka.admin import AdminClient, NewTopic

class KafkaTopics(object):

    def __init__(self, module):
      self.module = module
      conf = {
        'bootstrap.servers': module.params['bootstrap_servers'],
        'security.protocol': module.params['security_protocol']
      }
      self.client = AdminClient(conf)

    def create(self):
      print(self.module.params['partitions'])
      new_topics = [NewTopic(self.module.params['name'], num_partitions=self.module.params['partitions'], replication_factor=self.module.params['replication_factor'])]
      fs = self.client.create_topics(new_topics)

      for topic, f in fs.items():
        try:
          f.result()
          msg="Topic {} created".format(topic)
        except Exception as e:
          self.module.fail_json(msg="Failed to create topic {}: {}".format(topic, e))
      return msg

def main():
    arg_spec = dict(
        name=dict(required=True),
        state=dict(required=True, choices=['present', 'absent']),
        partitions=dict(default=1, type=int),
        replication_factor=dict(default=1, type=int),
        client_options=dict(required=False, default=None),
        config=dict(required=False, default=None),
        zookeeper=dict(required=False, default=None),
        bootstrap_servers=dict(required=False, default=None),
        security_protocol=dict(required=False, default=None),
        append=dict(required=False, default=True)
    )

    module = AnsibleModule(
        argument_spec=arg_spec,
        supports_check_mode=True
    )

    result = dict()

    state = module.params['state']

    kafka_topics = KafkaTopics(module)

    enabled = []
    disabled = []
    if state == 'present':
      stdout = kafka_topics.create()

    result['stdout'] = stdout
    result['changed'] = len(enabled) > 0 or len(disabled) > 0
    result['enabled'] = enabled
    result['disabled'] = disabled
    module.exit_json(**result)

if __name__ == '__main__':
    main()
