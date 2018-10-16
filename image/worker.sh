#!/bin/bash

source /opt/worker.env

gcloud logging write docker-worker "Docker task ${TASK_ID} started" --severity=WARNING

RESULT=`docker run $TASK_IMAGE`
# control return code? or handle errors inside app?

echo $RESULT

gcloud logging write docker-worker "${RESULT}" --severity=WARNING  # Global context
gcloud logging write docker-worker "Docker task ${TASK_ID} finished" --severity=WARNING
gcloud pubsub topics publish projects/${GCP_PROJECT}/topics/${REPORTING_TOPIC} --message "${TASK_ID}"

