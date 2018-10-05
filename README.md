FLOW:

external system -> pubsub topic / web hook -> cloud function (create/start worker instance) -> compute engine (pull details of task from the metadata server) -> docker execute (pull image from the registry) -> pubsub topic -> cloud function (destroy worker instance)

PARTS:

- image: packer stuff for a base image of the worker
- cloud_functions: source code of the functions

TODO:

- add docker stuff (registry, image)
- keep source of the functions in a gcp repository 
- terraform stuff to create/manage cloud functions, source repository, docker registry etc
