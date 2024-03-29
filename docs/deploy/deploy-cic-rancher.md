# Deploy the Netscaler ingress controller on a Rancher managed Kubernetes cluster

[Rancher](https://rancher.com/) is an open-source platform with an intuitive user interface that helps you to easily deploy and manage Kubernetes clusters. Rancher supports Kubernetes clusters on any infrastructure be on cloud or on-premises deployment. Rancher also allows you to centrally manage multiple clusters running across your organization.

 The [Netscaler ingress controller](/docs/index.md) is built around the Kubernetes [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) and it can automatically configure one or more Netscalers based on the Ingress resource configuration. You can deploy the Netscaler ingress controller in a Rancher managed Kubernetes cluster to extend the advanced load balancing and traffic management capabilities of Netscaler to your cluster.

## Prerequisites

You must create a Kubernetes cluster and import the cluster on the Rancher platform.

## Deployment options

 You can either deploy Netscaler CPXs as pods inside the cluster or deploy a Netscaler MPX or VPX appliance outside the Kubernetes cluster.

Based on how you want to use Netscaler, there are two ways to deploy the Netscaler ingress controller in a Kubernetes cluster on the Rancher platform:

-  As a sidecar container alongside Netscaler CPX in the same pod: In this mode, Netscaler ingress controller configures the Netscaler CPX.
  
-  As a standalone pod in the Kubernetes cluster: In this mode, you can control the Netscaler MPX or VPX appliance deployed outside the cluster.

## Deploy the Netscaler ingress controller as a sidecar with Netscaler CPX

In this deployment, you can use the Netscaler CPX instance for load balancing the North-South traffic to microservices in your Kubernetes cluster. Netscaler ingress controller is deployed as a sidecar alongside the Netscaler CPX container in the same pod using the `citrix-k8s-cpx-ingress.yaml` file.

Perform the following steps to deploy the Netscaler ingress controller as a sidecar with Netscaler CPX on the Rancher platform.

1.  Download the `citrix-k8s-cpx-ingress.yaml` file using the following command.

        wget  https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/baremetal/citrix-k8s-cpx-ingress.yml

1.  On the Rancher GUI cluster page, select Clusters from Global view.
1.  From the Clusters page, open the cluster that you want to access.
1.  Click `Launch kubectl` to open a terminal for interacting with your Kubernetes cluster.
1.  Create a file named `cpx.yaml` in the launched terminal and then copy the contents of the modified `citrix-k8s-cpx-ingress.yaml` file to the `cpx.yaml` file.
1.  Deploy the newly created YAML file using the following command.

            kubectl create -f cpx.yaml
1.  Verify if Netscaler ingress controller is deployed successfully using the following command.

        kubectl get pods --all-namespaces

## Deploy the Netscaler ingress controller as a standalone pod

In this deployment, Netscaler ingress controller which runs as a stand-alone pod allows you to control the Netscaler MPX, or VPX appliance from the Kubernetes cluster. You can use the `citrix-k8s-ingress-controller.yaml` file for this deployment.

**Before you begin:**

Ensure that you complete all the [prerequisites](deploy-cic-yaml.md#prerequisites) required for deploying the Netscaler ingress controller.

**To deploy the Netscaler ingress controller as a standalone pod on the Rancher platform:**

1.  Download the  `citrix-k8s-ingress-controller.yaml` file using the following command:

        wget https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/baremetal/citrix-k8s-ingress-controller.yaml

1.  Edit the `citrix-k8s-ingress-controller.yaml` file and enter the values of the environment variable using the information in [Deploy Netscaler ingress controller as a pod](deploy-cic-yaml.md#deploy-citrix-ingress-controller-as-a-pod).

     **Note:** To update the `Status.LoadBalancer.Ingress` field of the Ingress resources managed by the Netscaler ingress controller with the allocated IP addresses, you must specify the command line argument `--update-ingress-status yes` when you start the Netscaler ingress controller. For more information, see [Updating the Ingress status for the Ingress resources with the specified IP address](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/configure/ingress-classes/#updating-the-ingress-status-for-the-ingress-resources-with-the-specified-ip-address).

1.  On the Rancher GUI cluster page, select Clusters from Global view.
1.  From the Clusters page, open the cluster that you want to access.
1.  Click `Launch kubectl` to open a terminal for interacting with your Kubernetes cluster.
1.  Create a file named `cic.yaml` in the launched terminal and then copy the content of the modified `citrix-k8s-ingress-controller.yaml` file to `cic.yaml`.
1.  Deploy the `cic.yaml` file using the following command.

        kubectl create -f cic.yaml

1.  Verify if the Netscaler ingress controller is deployed successfully using the following command.

        kubectl get pods --all-namespaces
