#!/bin/bash

source /opt/worker.env

gcloud logging write docker-worker "Docker task ${TASK_ID} started" --severity=WARNING

SHARED_FILES="/tmp/worker"

mkdir ${SHARED_FILES}

if [ "$SHARED_BUCKET" != "$T2" ]; then
  gsutil rsync -r -d  gs://${SHARED_BUCKET}/ ${SHARED_FILES}
fi

RESULT=`su - ubuntu -s /bin/bash -c "source /opt/google-cloud-sdk/path.bash.inc && docker-credential-gcr configure-docker >/dev/null 2>&1 && docker run -v ${SHARED_FILES}:${SHARED_FILES} $TASK_IMAGE $TASK_ARGS"`
# control return code? or handle errors inside app?

echo $RESULT

gcloud logging write docker-worker "${RESULT}" --severity=WARNING  # Global context
gcloud logging write docker-worker "Docker task ${TASK_ID} finished" --severity=WARNING
gcloud pubsub topics publish projects/${GCP_PROJECT}/topics/${REPORTING_TOPIC} --message "${TASK_ID}"

