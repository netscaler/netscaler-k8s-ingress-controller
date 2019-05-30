## Introduction
Helm, the package manager for Kubernetes that contains information sufficient for installing, upgrading and managing a set of Kubernetes resources into a Kubernetes cluster. Helm packages are called charts. A Helm chart encapsulates YAML definitions, provides a mechanism for configuration at deploy-time and allows you to define metadata and documentation that might be useful when sharing the package.

Helm has two parts: a client (helm) and a server (tiller). Tiller is the in-cluster component of Helm. It interacts directly with the Kubernetes API server to install, upgrade, query, and remove Kubernetes resources. Tiller manages both, the releases (installations) and revisions (versions) of charts deployed on the cluster. When you run helm commands, your local Helm client sends instructions to tiller in the cluster that in turn make the requested changes.

## Installation
### `1`. Create an openshift project for tiller or use an already created project

(tiller is the serverside software)

in case of creating:
```oc new-project tiller```

in case of will to select an existing project:
```oc project {project name}```

## `2`. do `export TILLER_NAMESPACE=tiller` so the name of tiller's namespace environment variable is set into your shell session.

## `3`. Install helm client on your computer. 

Have a look at [helm releases page](https://github.com/helm/helm/releases) for newer releases. 
Please note your helm client and server deployment should be the same version.

Installing using package managers:

```
curl -s https://storage.googleapis.com/kubernetes-helm/helm-v2.12.1-linux-amd64.tar.gz | tar xz
cd linux-amd64
sudo cp helm /usr/local/bin && chmod +x /usr/local/bin/helm 
helm init --client-only
```

## `4`. Install the Tiller server

In principle this can be done using helm init, but currently the helm client doesn’t fully set up the service account rolebindings that OpenShift expects. To try to keep things simple, we’ll use a pre-prepared OpenShift template instead created by [RedHat](https://www.redhat.com/en) people. The template sets up a dedicated service account for the Tiller server, gives it the necessary permissions, then deploys a Tiller pod that runs under the newly created SA.

Get the file.
```wget -q https://github.com/openshift/origin/raw/master/examples/helm/tiller-template.yaml```

Add clusterRoleBinding required to deploy Citrix ingress Controller.

```
- kind: ClusterRoleBinding
  apiVersion: rbac.authorization.k8s.io/v1
  metadata:
    name: tiller
  roleRef:
    apiGroup: rbac.authorization.k8s.io
    kind: ClusterRole
    name: cluster-admin
  subjects:
    - kind: ServiceAccount
      name: tiller
      namespace: ${TILLER_NAMESPACE}
```

Deploy the yaml:

```oc process -f tiller-template.yaml -p TILLER_NAMESPACE="${TILLER_NAMESPACE}" -p HELM_VERSION=v2.12.1 | oc create -f -```

> NOTE: Again, please note helm client and server versions should be the same. 

Then:
```
 oc rollout status deployment tiller
```
Make sure the deployment is successfully rolled out. 


## Verify
You can verify that you have the correct version and that it installed properly by running:

   ```helm version ```

If helm is initialised properly you will get output for helm version something like:

   ```
   Client: &version.Version{SemVer:"v2.12.1", GitCommit:"02a47c7249b1fc6d8fd3b94e6b4babf9d818144e", GitTreeState:"clean"}
   Server: &version.Version{SemVer:"v2.12.1", GitCommit:"02a47c7249b1fc6d8fd3b94e6b4babf9d818144e", GitTreeState:"clean"}
   ```
