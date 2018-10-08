import time
import datetime
import os

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from pprint import pprint


def hello_world(request):
    credentials = GoogleCredentials.get_application_default()

    service = discovery.build('compute', 'v1', credentials=credentials)

    project = os.environ.get('GCP_PROJECT', '')
    zone = os.environ.get('WORKER_ZONE', '')
    type = os.environ.get('WORKER_TYPE', '')
    family = os.environ.get('WORKER_IMAGE', '')
    docker_image = os.environ.get('TASK_IMAGE', 'hello-world')
    task_id = '{0}-{1}-{2}'.format(
        family,
        datetime.date.today(),
        int(time.time()))

    image_response = service.images().getFromFamily(
        project=project, family=family).execute()
    source_disk_image = image_response['selfLink']

    instance_body = {
        "kind": "compute#intance",
        "name": task_id,
        'machineType': 'projects/{0}/zones/{1}/machineTypes/{2}'.format(project, zone, type),
        'disks': [
            {
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': source_disk_image,
                }
            }
        ],
        'networkInterfaces': [{
            'network': 'global/networks/default',
            'accessConfigs': [
                {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
            ]
        }],
        'serviceAccounts': [{
            'email': 'default',
            'scopes': [
                'https://www.googleapis.com/auth/devstorage.read_write',
                'https://www.googleapis.com/auth/logging.write',
                'https://www.googleapis.com/auth/pubsub'
            ]
        }],
        'metadata': {
            'items': [
                {
                    'key': 'startup-script',
                    'value': '#!/bin/bash\n\n/opt/worker.sh'
                },
                {
                    'key': 'project',
                    'value': project
                },
                {
                    'key': 'reporting_topic',
                    'value': 'task_finished'
                },
                {
                    'key': 'task_image',
                    'value': docker_image
                },
                {
                    'key': 'task_id',
                    'value': task_id
                }
            ]
        }
    }

    request = service.instances().insert(project=project, zone=zone, body=instance_body)
    response = request.execute()

    pprint(response)