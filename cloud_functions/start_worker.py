import time

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from pprint import pprint


def start_worker(request):
    credentials = GoogleCredentials.get_application_default()

    service = discovery.build('compute', 'v1', credentials=credentials)

    project = 'pacific-vault-218409'  # TODO: Update placeholder value.
    zone = 'us-east1-b'
    family = 'docker-worker'	

    image_response = service.images().getFromFamily(
        project=project, family=family).execute()
    source_disk_image = image_response['selfLink']
    
    instance_body = {
        "kind": "compute#intance",
        "name": family + str(int(time.time())),
        'machineType': 'projects/{0}/zones/{1}/machineTypes/{2}'.format(prohect, zone, 'f1-micro'),
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
                'https://www.googleapis.com/auth/logging.write'
            ]
        }],
        'metadata': {
            'items': [
                {
                    'key': 'frutik',
                    'value': 'frutik'
                }
            ]
        }
    }

    request = service.instances().insert(project=project, zone=zone, body=instance_body)
    response = request.execute()

    # TODO: Change code below to process the `response` dict:
    pprint(response)
