## Introduction
Helm, the package manager for Kubernetes that contains information sufficient for installing, upgrading and managing a set of Kubernetes resources into a Kubernetes cluster. Helm packages are called charts. A Helm chart encapsulates YAML definitions, provides a mechanism for configuration at deploy-time and allows you to define metadata and documentation that might be useful when sharing the package.

Helm has two parts: a client (helm) and a server (tiller). Tiller is the in-cluster component of Helm. It interacts directly with the Kubernetes API server to install, upgrade, query, and remove Kubernetes resources. Tiller manages both, the releases (installations) and revisions (versions) of charts deployed on the cluster. When you run helm commands, your local Helm client sends instructions to tiller in the cluster that in turn make the requested changes.

## Installation
To install Helm run Helm's installer script in a terminal:

```
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get > get_helm.sh
chmod 700 get_helm.sh
./get_helm.sh
```

There are several other ways to install Helm as well, you can find it [here](https://docs.helm.sh/using_helm/#installing-helm).

## Initialization
After installing helm on your machine, initialize Helm on your Kubernetes cluster:

   1. If you are using Kubernetes version v1.16 or later please do the following otherwise skip this step: <br />
      Helm init command generates a "tiller.yaml" and applies the same on the cluster. However, it generates tiller deployment with apiVersion "extensions/v1beta1" which is not supported anymore from kubernetes version v1.16 onwards. So, delete the default tiller deployment and create the new one with updated apiVersion:

      ```
      kubectl delete deployment tiller-deploy -n kube-system
      kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/charts/tiller.yaml
      ```

   2. Set up a ServiceAccount for use by tiller.

      ```
      kubectl --namespace kube-system create serviceaccount tiller
      ```

   3. Give the ServiceAccount full permissions to manage the cluster.

      ```
      kubectl create clusterrolebinding tiller --clusterrole cluster-admin --serviceaccount=kube-system:tiller
      ```

   4. Initialize helm and tiller.

      ```helm init --service-account tiller --upgrade```

## Verify
You can verify that you have the correct version and that it installed properly by running:

   ```helm version ```

If helm is initialised properly you will get output for helm version something like:

   ```
	Client: &version.Version{SemVer:"v2.14.3", GitCommit:"0e7f3b6637f7af8fcfddb3d2941fcc7cbebb0085", GitTreeState:"clean"}
	Server: &version.Version{SemVer:"v2.14.3", GitCommit:"0e7f3b6637f7af8fcfddb3d2941fcc7cbebb0085", GitTreeState:"clean"}
   ```
