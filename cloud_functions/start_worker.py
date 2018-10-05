import time
import os

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from pprint import pprint


def start_worker(request):
    credentials = GoogleCredentials.get_application_default()

    service = discovery.build('compute', 'v1', credentials=credentials)

    project = os.environ.get('GCP_PROJECT', '') 
    worker_zone = os.environ.get('WORKER_ZONE', '')
    worker_type = os.environ.get('WORKER_TYPE', '')
    worker_family = os.environ.get('WORKER_IMAGE', '')
    task_id = family + '-' + str(int(time.time()))

    image_response = service.images().getFromFamily(
        project=project, family=worker_family).execute()
    source_disk_image = image_response['selfLink']
    
    instance_config = {
        "kind": "compute#intance",
        "name": task_id,
        'machineType': 'projects/{0}/zones/{1}/machineTypes/{2}'.format(prohect, worker_zone, worker_type),
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
                    'key': 'task_id',
                    'value': task_id
                }            
	    ]
        }
    }

    request = service.instances().insert(project=project, zone=worker_zone, body=instance_config)
    response = request.execute()

    # TODO: Change code below to process the `response` dict:
    pprint(response)
