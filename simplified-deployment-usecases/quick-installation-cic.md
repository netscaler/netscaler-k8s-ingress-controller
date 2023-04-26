# Quick reference for Citrix ingress controller deployment

This topic provides a quick reference on how to deploy [Citrix ingress controller](citrix-k8s-ingress-controller) on on-prem and cloud based Kubernetes environments. This topic contains the following sections.

-  [On-prem deployment of Citrix ingress controller for NetScaler VPX or MPX](#on-prem-deployment-of-citrix-ingress-controller-for-netscaler-vpx-or-mpx)

-  [On-prem deployment of Citrix ingress controller for NetScaler CPX](#on-prem-deployment-of-citrix-ingress-controller-for-netscaler-cpx)

-  [Deployment of Citrix ingress controller on the OpenShift platform](#deployments-on-the-openshift-platform)

-  [Deployment of Citrix ingress controller on public cloud platforms](#deployment-of-citrix-ingress-controller-on-public-clouds)

    -  [Deploy Citrix ingress controller on the Azure Kubernetes Service (AKS) cluster](#deployment-on-azure-kubernetes-service-aks)

    -  [Deploy Citrix ingress controller on the Amazon Elastic Kubernetes Service (EKS) cluster](#deploy-citrix-ingress-controller-on-amazon-elastic-kubernetes-service-eks)

    -  [Deploy Citrix ingress controller on the Google Kubernetes Engine (GKE) cluster](#deploy-citrix-ingress-controller-on-google-kubernetes-engine-gke)

## General information

In the procedures in this topic:

-  Citrix ingress controller is installed in the `netscaler` namespace.

-  Citrix ingress controller is created with the ingress class `netscaler`. This step ensures that Citrix ingress controller listens to Ingress resources associated with the `netscaler` ingress class only. For more information, see the [Ingress class documentation](https://docs.citrix.com/en-us/citrix-k8s-ingress-controller/configure/ingress-classes.html).

-  Citrix ingress controller manages the NetScaler appliance that can be deployed in various modes. See, [deployment topologies](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/deployment-topologies.md) for better understanding of Citrix ingress controller and NetScaler topologies.

## On-prem deployment of Citrix ingress controller for NetScaler VPX or MPX

### Prerequisites

-  Ensure that the network connectivity between NetScaler and the pod network of the Kubernetes cluster is established. It enables the Citrix ingress controller to configure NetScaler.
Follow [static-routing guide](https://docs.citrix.com/en-us/citrix-k8s-ingress-controller/network/staticrouting.html) or [Citrix Node Controller guide](https://docs.citrix.com/en-us/citrix-k8s-ingress-controller/network/node-controller.html) for establishing the network connectivity.

-  Ensure that an account for user name `Citrix ingress controller` is created on the NetScaler appliance. Follow the steps in [Create NetScaler user account](https://github.com/citrix/citrix-helm-charts/tree/master/citrix-ingress-controller#create-system-user-account-for-citrix-ingress-controller-in-citrix-adc) to create the account on the NetScaler.

### Deploy Citrix ingress controller for NetScaler VPX or MPX using Helm Charts

To deploy Citrix ingress controller for NetScaler VPX or MPX in the `netscaler` namespace, use the following commands:

```
helm repo add citrix https://citrix.github.io/citrix-helm-charts/

kubectl create namespace netscaler 

kubectl create secret generic nslogin --from-literal=username='Citrix ingress controller' --from-literal=password='mypassword' -n netscaler

helm install Citrix ingress controller citrix/citrix-ingress-controller --set nsIP=<NSIP>,license.accept=yes,crds.install=true,ingressClass[0]=netscaler --set adcCredentialSecret=nslogin --namespace netscaler

```

While using these commands the assumption is that the credentials of the NetScaler appliance are `Citrix ingress controller` and `mypassword`. Provide the appropriate input for the credentials while creating the Kubernetes secret. Also, `nsIP` represents the management IP address of the NetScaler appliance and can be one of the following:

-  [NSIP](https://docs.citrix.com/en-us/citrix-adc/current-release/networking/ip-addressing/configuring-citrix-adc-owned-ip-addresses/configuring-citrix-adc-ip-address.html) - For standalone NetScaler

-  [SNIP](https://docs.citrix.com/en-us/citrix-adc/current-release/networking/ip-addressing/configuring-citrix-adc-owned-ip-addresses/configuring-subnet-ip-addresses-snips.html) with management access enabled - For NetScaler HA pair

-  [CLIP](https://docs.citrix.com/en-us/citrix-adc/current-release/clustering/cluster-overview/ip-addressing.html) - For NetScaler cluster

#### Using Citrix Deployment Builder to generate the values file

Helm expects arguments or the [values.yaml](https://helm.sh/docs/chart_template_guide/values_files/) file to be specified in the command line. Citrix provides a GUI tool [Citrix Deployment Builder](https://citrix.github.io/citrix-k8s-ingress-controller/) to generate the `values.yaml` file that can be given in the Helm command.

The following commands can be used to deploy the Citrix ingress controller with the generated `values.yaml` file.

```
helm repo add citrix https://citrix.github.io/citrix-helm-charts/

helm install Citrix ingress controller citrix/citrix-cloud-native -f values.yaml 
```

### Deploy Citrix ingress controller for NetScaler VPX or MPX using the YAML manifest

For installing Citrix ingress controller the Helm chart installation is preferred. However, in case the Helm chart is unavailable, Citrix ingress controller can be installed using the YAML file.

**Note:** Ensure that the environment variable `NS_IP` in the given YAML file is set to the management IP address of the NetScaler appliance.

Use the following commands for YAML deployment:

```
kubectl create namespace netscaler 

kubectl create secret generic nslogin --from-literal=username='Citrix ingress controller' --from-literal=password='mypassword' -n netscaler

kubectl create -n netscaler -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/baremetal/citrix-k8s-ingress-controller.yaml

```

## On-prem deployment of Citrix ingress controller for NetScaler CPX

You can deploy Citrix ingress controller for NetScaler CPX in the `netscaler` name space using Helm charts or the YAML manifest.

### Deploy Citrix ingress controller and NetScaler CPX using Helm Charts

Use the following commands to deploy Citrix ingress controller and NetScaler CPX using Helm charts.

```
helm repo add citrix https://citrix.github.io/citrix-helm-charts/

kubectl create namespace netscaler

helm install citrix-cpx-with-ingress-controller citrix/citrix-cpx-with-ingress-controller --set license.accept=yes,crds.install=true,ingressClass[0]=netscaler --namespace netscaler
```

### Deploy Citrix ingress controller and NetScaler CPX using the YAML file

Perform the following steps to deploy Citrix ingress controller and NetScaler CPX using the YAML file.

```
kubectl create namespace netscaler

kubectl create -n netscaler -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/baremetal/citrix-k8s-cpx-ingress.yml
```

## Deployments on the OpenShift Platform

Citrix ingress controller can be deployed on the OpenShift environment using Helm charts or OpenShift Operator.

### Using Helm charts

#### Deploy Citrix ingress controller for NetScaler VPX or MPX using Helm Charts

Use the following commands for deployment using Helm charts:

```
helm repo add citrix https://citrix.github.io/citrix-helm-charts/

kubectl create namespace netscaler 

kubectl create secret generic nslogin --from-literal=username='Citrix ingress controller' --from-literal=password='mypassword' -n netscaler

helm install Citrix ingress controller citrix/citrix-ingress-controller --set nsIP=<NSIP>,license.accept=yes,crds.install=true,ingressClass[0]=netscaler --set adcCredentialSecret=nslogin --set openshift=true --namespace netscaler

oc adm policy add-scc-to-user privileged system:serviceaccount:<namespace>:<service-account-name>

```

The `oc adm policy add-scc-to-user privileged system:serviceaccount: <namespace>:<service-account-name>` command adds the name of the service account created when the chart is deployed to the privileged [Security Context Constraints](https://docs.openshift.com/container-platform/4.7/authentication/managing-security-context-constraints.html) of OpenShift.

#### Deploy Citrix ingress controller and NetScaler CPX using Helm Charts

Use the following commands for deployment using Helm charts:

```
helm repo add citrix https://citrix.github.io/citrix-helm-charts/

helm install citrix-cpx-with-ingress-controller citrix/citrix-cpx-with-ingress-controller --set license.accept=yes,crds.install=true,ingressClass[0]=netscaler --set openshift=true --namespace netscaler

oc adm policy add-scc-to-user privileged system:serviceaccount:<namespace>:<service-account-name>
```

The last command adds the name of the service account created when the chart is deployed to the privileged [Security Context Constraints](https://docs.openshift.com/container-platform/4.7/authentication/managing-security-context-constraints.html) of OpenShift.

### Using the OpenShift Operator

#### Deploy Citrix ingress controller for NetScaler VPX or MPX using the OpenShift operator

Follow the steps in [Deploy the Citrix ingress controller using OpenShift Operators](https://docs.netscaler.com/en-us/citrix-k8s-ingress-controller/deploy/cic-openshift-operator.html#deploy-the-citrix-ingress-controller-as-a-standalone-pod-in-the-openshift-cluster-for-citrix-adc-mpx-or-vpx-appliances) to deploy the Citrix ingress controller as a standalone pod in the OpenShift cluster for Citrix ADC MPX or VPX appliances.

#### Deploy Citrix ingress controller for NetScaler CPX using the OpenShift operator

Follow the steps in [Deploy the Citrix ingress controller as a sidecar with Citrix ADC CPX](https://docs.citrix.com/en-us/citrix-k8s-ingress-controller/deploy/Citrix-ingress-controller-openshift-operator.html#deploy-the-citrix-ingress-controller-as-a-sidecar-with-citrix-adc-cpx) to deploy the Citrix ingress controller for NetScaler CPX.

## Deployment of Citrix ingress controller on public clouds

Citrix ingress controller can be deployed on managed Kubernetes services of Azure (AKS), AWS (EKS), and GCP (GKE).

### Deployment on Azure Kubernetes Service (AKS)

Ensure that you have a Kubernetes cluster up and running. For information on creating an AKS cluster, see, [Create a Kubernetes cluster using Azure Kubernetes Engine](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/azure/create-aks/README.md).

#### Deploy Citrix ingress controller for NetScaler VPX on AKS

**Prerequisites**

-  Ensure that the NetScaler VPX instance is running on Azure. For more information on how to create a NetScaler VPX instance from Azure Marketplace, see [Create a Citrix ADC VPX instance from Azure Marketplace](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/deploy/azure-vpx.md).

-  You require a valid Azure Marketplace account and subscription.

Citrix ingress controller can be deployed the same way as mentioned in [On-prem deployment of Citrix ingress controller for NetScaler VPX or MPX](#on-prem-deployment-of-citrix-ingress-controller-for-netscaler-vpx-or-mpx). However, you need to first generate a URL for the Citrix ingress controller image that needs to be provided in the Helm chart or the YAML file.

Following are the minimal steps needed to deploy Citrix ingress controller for NetScaler VPX on AKS. For the detailed guide, see [Deploy Citrix ingress controller in an Azure Kubernetes Service cluster with Citrix ADC VPX](https://docs.citrix.com/en-us/citrix-k8s-ingress-controller/deploy/azure-cic.html).

1.  Follow the steps in [Generate a URL for the Citrix ingress controller image in Azure Marketplace](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/deploy/azure-cic-url.md) guide to generate a URL for the Citrix ingress controller from the Azure Marketplace.

2.  Once a registry is created, the Citrix ingress controller registry name should be attached to the AKS cluster used for deployment.

    ```
    az aks update -n <cluster-name> -g <resource-group-where-aks-deployed> --attach-acr <Citrix ingress controller-registry>

    ```

3.  Establish the network connectivity between the NetScaler VPX and the pod network of the Kubernetes cluster.

    ```
    add ns ip <snip-vpx-instance-private-ip> <vpx-instance-primary-ip-subnet>
    ```

    Where:
    `snip-vpx-instance-private-ip` is the dynamic private IP address assigned while adding a SNIP during the NetScaler VPX instance creation.

    `vpx-instance-primary-ip-subnet` is the subnet of the primary private IP address of the NetScaler VPX instance.

4.  - Deploy using YAML

        To deploy Citrix ingress controller using the YAML manifest, follow the steps in [Deploy Citrix ingress controller in an Azure Kubernetes Service cluster with Citrix ADC VPX](https://docs.netscaler.com/en-us/citrix-k8s-ingress-controller/deploy/azure-cic.html#deploy-citrix-ingress-controller).

    or

    -  Deploy using Helm charts

        To deploy Citrix ingress controller in the `netscaler` namespace, use the following commands:

        ```
        helm repo add citrix https://citrix.github.io/citrix-helm-charts/

        kubectl create secret generic nslogin --from-literal=username='Citrix ingress controller' --from-literal=password='mypassword' -n netscaler

        helm install Citrix ingress controller citrix/citrix-ingress-controller --set nsIP=<NSIP-i.e.-primary-private-ip-addess-of-VPX> --set nsVIP=<private-IP-address-of-the-VIP-assigned-during-VPX-Azure-instance-creation> --set image=<azure-Citrix ingress controller-image-url-from-step-1> --set license.accept=yes,crds.install=true,ingressClass[0]=netscaler --set adcCredentialSecret=nslogin --namespace netscaler

        ```

### Deploy Citrix ingress controller and NetScaler CPX on AKS

#### Using the YAML manifest

Use the following commands to deploy using the YAML manifest.

```
kubectl create namespace netscaler

kubectl create -n netscaler -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/azure/manifest/standalone_cpx.yaml

kubectl create -n netscaler -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/azure/manifest/cpx_service.yaml

```

For detailed info regarding deployment of Citrix ingress controller and NetScaler CPX as an ingress in AKS, see [Deploy Citrix ADC CPX as an Ingress device in an Azure Kubernetes Service cluster](https://docs.citrix.com/en-us/citrix-k8s-ingress-controller/deploy/azure.html).

#### Using Helm charts

Use the following commands to deploy using Helm charts.

```
helm repo add citrix https://citrix.github.io/citrix-helm-charts/

helm install citrix-cpx-with-ingress-controller citrix/citrix-cpx-with-ingress-controller --set license.accept=yes,crds.install=true,ingressClass[0]=netscaler --set serviceType.loadBalancer.enabled=true --namespace netscaler
```

**Note:** If you want to use the Azure repo images of Citrix ingress controller and NetScaler CPX, use the following command.

```
helm install citrix-cpx-with-ingress-controller citrix/citrix-cpx-with-ingress-controller --set license.accept=yes,crds.install=true,ingressClass[0]=netscaler --set serviceType.loadBalancer.enabled=true --set image=<azure-cpx-instance-url>,Citrix ingress controller.image=<azure-Citrix ingress controller-instance-url> --set  --namespace netscaler
```

Follow the steps in [Get Citrix ADC CPX from Azure Marketplace](https://docs.citrix.com/en-us/citrix-k8s-ingress-controller/deploy/azure-image.html)  to create an image registry on Azure and to fetch the appropriate NetScaler CPX and Citrix ingress controller images.

## Deploy Citrix ingress controller on Amazon Elastic Kubernetes Service (EKS)

### Deploy Citrix ingress controller for NetScaler VPX, MPX on EKS

#### Using Helm charts

Follow the steps in [deploy Citrix ingress controller as a service of type LoadBalancer in AWS to manage NetScaler VPX](https://docs.citrix.com/en-us/citrix-k8s-ingress-controller/configure/service-type-lb-solution-in-aws.html#deploy-citrix-solution-for-service-of-type-loadbalancer-in-aws-using-helm-charts).

#### Using the YAML manifest

In case you want to use the YAML manifest, follow the steps in [deploy Citrix ingress controller as a service of type LoadBalancer in AWS to manage NetScaler VPX](https://docs.citrix.com/en-us/citrix-k8s-ingress-controller/configure/service-type-lb-solution-in-aws.html#deploy-citrix-solution-for-service-of-type-loadbalancer-in-aws-using-yaml).

### Deploy Citrix ingress controller and NetScaler CPX together on EKS

#### Using the YAML manifest

Use the following commands to deploy using the YAML manifest.

```
kubectl create namespace netscaler

kubectl create -n netscaler -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/aws/manifest/standalone_cpx.yaml

kubectl create -n netscaler -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/aws/manifest/cpx_service.yaml

```

For detailed information, see [Deployment of Citrix ingress controller and NetScaler CPX as an ingress in EKS](https://docs.citrix.com/en-us/citrix-k8s-ingress-controller/deploy/eks-cpx.html).

#### Using Helm charts

Use the following commands to deploy using Helm charts.

```
helm repo add citrix https://citrix.github.io/citrix-helm-charts/

helm install citrix-cpx-with-ingress-controller citrix/citrix-cpx-with-ingress-controller --set license.accept=yes,crds.install=true,ingressClass[0]=netscaler --set serviceType.loadBalancer.enabled=true --namespace netscaler
```

## Deploy Citrix ingress controller on Google Kubernetes Engine (GKE)

### Deploy Citrix ingress controller for NetScaler VPX, MPX on GKE

#### Prerequisites

-  Deploy NetScaler VPX instance on Google cloud. See [Deploying NetScaler VPX instance on Google cloud](https://github.com/citrix/citrix-ingress-controller-gcp-marketplace#deploying-a-citrix-adc-vpx-instance-on-google-cloud).

-  Create all the necessary components (VPC, GKE cluster, VPX creation on GCP) in the GKE before deploying the Citrix ingress controller. For more information, see the [Documentation for Citrix ingress controller hosted on the GCP Marketplace](https://github.com/citrix/citrix-ingress-controller-gcp-marketplace).

#### Using Helm charts

Use the following commands to deploy using Helm charts.

```
helm repo add citrix https://citrix.github.io/citrix-helm-charts/

kubectl create namespace netscaler

kubectl create secret generic nslogin --from-literal=username='Citrix ingress controller' --from-literal=password='mypassword' -n netscaler

helm install Citrix ingress controller citrix/citrix-ingress-controller --set nsIP=<NSIP-of-VPX-instance_OR_SNIP-with-management-access-enabled> --set nsVIP=<private-IP-address-of-the-VIP-assigned-during-VPX-instance-creation> --set license.accept=yes,crds.install=true,ingressClass[0]=netscaler --set adcCredentialSecret=nslogin --namespace netscaler
```

### Deploy Citrix ingress controller and NetScaler CPX on GKE

This section provides minimal steps to deploy NetScaler CPX as an ingress device in the Google Kubernetes Engine (GKE). It creates a NetScaler CPX service of the type `LoadBalancer` with an external IP address for receiving traffic.

#### Using the YAML manifest

Use the following commands to deploy using the YAML manifest:

```
kubectl create clusterrolebinding citrix-cluster-admin --clusterrole=cluster-admin --user=<email-id of your google account>

kubectl create namespace netscaler

kubectl create -n netscaler -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/gcp/manifest/standalone_cpx.yaml

kubectl create -n netscaler -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/gcp/manifest/cpx_service.yaml

```

For detailed information on deploying Citrix ingress controller and NetScaler CPX as an ingress in GKE, see the [GCP guide](https://docs.citrix.com/en-us/citrix-k8s-ingress-controller/deploy/gcp.html).

#### Using Helm charts

Use the following commands to deploy using Helm charts.

```
helm repo add citrix https://citrix.github.io/citrix-helm-charts/

helm install citrix-cpx-with-ingress-controller citrix/citrix-cpx-with-ingress-controller --set license.accept=yes,crds.install=true,ingressClass[0]=netscaler --set serviceType.loadBalancer.enabled=true --namespace netscaler
```