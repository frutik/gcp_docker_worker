#!/bin/bash

apt-get update
apt-get install -y docker.io

cd /opt
wget https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-220.0.0-linux-x86_64.tar.gz
tar zxvf google-cloud-sdk-220.0.0-linux-x86_64.tar.gz google-cloud-sdk
./google-cloud-sdk/install.sh -q
source /opt/google-cloud-sdk/path.bash.inc && gcloud components install -q docker-credential-gcr
source /opt/google-cloud-sdk/path.bash.inc && docker-credential-gcr configure-docker

chmod +x /opt/worker.sh
