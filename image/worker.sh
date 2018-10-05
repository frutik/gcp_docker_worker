#!/bin/bash

GCP_PROJECT=$(curl http://metadata/computeMetadata/v1/instance/attributes/project -H "Metadata-Flavor: Google")
TASK_ID=$(curl http://metadata/computeMetadata/v1/instance/attributes/task_id -H "Metadata-Flavor: Google")
REPORTING_TOPIC=$(curl http://metadata/computeMetadata/v1/instance/attributes/reporting_topic -H "Metadata-Flavor: Google")

# start docker process

gcloud logging write docker-worker "Docker task ${TASK_ID} started" --severity=WARNING

sleep 5m  # docker exec here. control return code? or handle errors inside app?

# log and send signal to destroy this instance

gcloud logging write docker-worker "Docker task ${TASK_ID} finished" --severity=WARNING
gcloud pubsub topics publish projects/${GCP_PROJECT}/topics/${REPORTING_TOPIC} --message 'test'
