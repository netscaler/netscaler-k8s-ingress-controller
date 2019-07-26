# Upgrade Citrix ingress controller

This topic explains how to upgrade the Citrix ingress controller instance for Citrix ADC CPX with Citrix ingress controller as sidecar and Citrix ingress controller standalone deployments.

## Upgrade Citrix ADC CPX with Citrix ingress controller as a sidecar

To upgrade a Citrix ADC CPX with Citrix ingress controller as a sidecar, you can either modify the associated YAML definition file (for example, [citrix-k8s-cpx-ingress.yml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/baremetal/citrix-k8s-cpx-ingress.yml)) or use the Helm chart.

If you want to upgrade by modifying the YAML defination file, perform the following:

1.  Change the version of the Citrix ingress controller and Citrix ADC CPX image under `containers` to the following:
    -  Citrix ADC CPX version: 13.0-36.29 (`quay.io/citrix/citrix-k8s-cpx-ingress:13.0-36.29`)
    -  Citrix ingress controller version: 1.2.0 (`quay.io/citrix/citrix-k8s-cpx-ingress:13.0-36.29`)
  
1.  Update the `CluterRole` as follows:

    ```yml
    kind: ClusterRole
    apiVersion: rbac.authorization.k8s.io/v1beta1
    metadata:
      name: cic-k8s-role
    rules:
      - apiGroups: [""]
        resources: ["services", "endpoints", "ingresses", "pods", "secrets", "routes", "routes/status", "nodes", "namespaces"]
        verbs: ["*"]
      - apiGroups: ["extensions"]
        resources: ["ingresses", "ingresses/status"]
        verbs: ["*"]
      - apiGroups: ["citrix.com"]
        resources: ["rewritepolicies", "vips"]
        verbs: ["*"]
      - apiGroups: ["apps"]
        resources: ["deployments"]
        verbs: ["*"]
      - apiGroups: ["apiextensions.k8s.io"]
        resources: ["customresourcedefinitions"]
        verbs: ["get", "list", "watch"]
    ```

1.  Save the YAML defination file and re-apply the file.

## Upgrade a standalone Citrix ingress controller to version 1.2.0

To upgrade a standalone Citrix ingress controller instance, you can either modify the YAML definition file or use the Helm chart.

If you want to upgrade Citrix ingress controller to version 1.2.0 by modifying the YAML defination file, perform the following:

1.  Change the version for the Citrix ingress controller image under `containers`. For example, consider you have the following YAML file.

    ```YAML
    apiVersion: v1
    kind: Pod
    metadata:
      name: cic-k8s-ingress-controller

      labels:
        app: ...
    spec:
          serviceAccountName: ...
          containers:
          - name: cic-k8s-ingress-controller
            image: "quay.io/citrix/citrix-k8s-ingress-controller:0.1.3"
            env: ...
            args: ...

    ```

    You should change the version of the image to version 1.2.0. For example, `quay.io/citrix/citrix-k8s-ingress-controller:1.2.0`.

1.  Update the `CluterRole` as follows:

    ```yml
    kind: ClusterRole
    apiVersion: rbac.authorization.k8s.io/v1beta1
    metadata:
      name: cic-k8s-role
    rules:
      - apiGroups: [""]
        resources: ["services", "endpoints", "ingresses", "pods", "secrets", "routes", "routes/status", "nodes", "namespaces"]
        verbs: ["*"]
      - apiGroups: ["extensions"]
        resources: ["ingresses", "ingresses/status"]
        verbs: ["*"]
      - apiGroups: ["citrix.com"]
        resources: ["rewritepolicies", "vips"]
        verbs: ["*"]
      - apiGroups: ["apps"]
        resources: ["deployments"]
        verbs: ["*"]
      - apiGroups: ["apiextensions.k8s.io"]
        resources: ["customresourcedefinitions"]
        verbs: ["get", "list", "watch"]
    ```

1.  Save the YAML defination file and re-apply the file.
