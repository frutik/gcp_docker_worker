#!/bin/bash

source /opt/worker.env

gcloud logging write docker-worker "Docker task ${TASK_ID} started" --severity=WARNING

RESULT=`sudo docker run $TASK_IMAGE`
# control return code? or handle errors inside app?

gcloud logging write docker-worker "${RESULT}" --severity=WARNING
gcloud logging write docker-worker "Docker task ${TASK_ID} finished" --severity=WARNING
gcloud pubsub topics publish projects/${GCP_PROJECT}/topics/${REPORTING_TOPIC} --message "${TASK_ID}"

