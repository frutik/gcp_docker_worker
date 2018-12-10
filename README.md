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

HOWTOs

## If you wanna have some files (for example custom ssl certs for the encription) inside a docker container

- Create bucket on the storage. For example gs://ssl-certs
- Upload files into thsi bucket
- For the cloud function create_worker add methadata variable SHARED_BUCKE="ssl-certs"
- Content of the bucket will be availabe inside the docker container in a folder /tmp/worker

## If you wanna pass some data into an application inside of a docker container

Do this with the environment variables. 

- First of all, update metadata section of the cloud function which lunches the worker instance. 
- Add support for the convertion of a value from the instance's metadata into env variable (see image/worker.env file).
- Build new image for the worker (with the support of this new variable). 
- Add support for the new variable in an application inside a docker container
- Rebuild/push new docker image into repository

