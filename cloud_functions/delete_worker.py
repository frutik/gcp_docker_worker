import base64
import os
import google.cloud.logging

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials


def main(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    name = base64.b64decode(event['data']).decode('utf-8')

    client = google.cloud.logging.Client()
    client.setup_logging()

    import logging

    credentials = GoogleCredentials.get_application_default()

    service = discovery.build('compute', 'v1', credentials=credentials)

    project = os.environ.get('GCP_PROJECT', '')
    zone = os.environ.get('WORKER_ZONE', '')

    try:
        r = service.instances().delete(project=project, zone=zone, instance=name).execute()
        logging.error(r)
    except Exception as e:
        logging.error(e)
