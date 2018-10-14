TASK:

- start high performant (and expensive) instance
- pull docker image with a worker application
- do the job
- shutdown the instance as soon as job done
- profit

FLOW:

external system -> pubsub topic / web hook (request to start job's execution) -> cloud function (create/start worker instance, pull details of the insance from the metadata server) -> compute engine (pull details of task from the metadata server) -> docker execute (pull image from the registry) -> pubsub topic -> cloud function (destroy worker instance)

PARTS:

- image: packer stuff for a base image of the worker (adds mostly docker support and cloud-init stuff)
- cloud_functions: source code of the functions

TODO:

- keep source of the functions in a gcp repository 
- terraform stuff to create/manage cloud functions, source repository, docker registry etc
- understand how to track if docker exec was succesfull (handle exit codes of docker?)

HOW TO INSTALL MANUALLY

- create service account with EDITOR permissions
- create/download json key credentianl. save it as image/account.json
- build base image cd image && PROJECT_ID="your-project-id" ACCOUNT_FILE="account.json" ZONE="us-west1-a" ./build-images.sh
- create two cloud functions
- MORE IS COMMING
