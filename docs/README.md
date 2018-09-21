CitrixIngressController (Citrix Ingress Controller)
The Citrix® NetScaler Ingress Controller allows you to configure and monitor the NetScaler appliance programmatically in Kubernetes, Docker Swarm, MesoS enviornment.

This readme briefly explains the directory structure of this Micro Service.

Directory Structure
build - All Files required for building the micro service image.
doc - Contains the API reference and a getting started guide.
tests - Contains test cases.
src - Contains the Citrix Ingress Controller source code.
Installation
There are two ways you can install Citrix Ingress Controller.

Pull the complete code into your machine and do appropriate build from build folder which creates a image. Load this docker image and use it.

Already the image has been pushed to public repository, you can get these by running

kubectl create -f citrix-ingress-controller.yml

License
Citrix Ingress Controller is a free software. You can redistribute and modify it under the terms of the Apache License. See LICENSE.txt for details.

Prefered Python Version
This Citrix Ingress Controller Micro service is developed using python v2.7.12
