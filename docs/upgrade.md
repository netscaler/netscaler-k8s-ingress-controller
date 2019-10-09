# Upgrade Citrix ingress controller

This topic explains how to upgrade the Citrix ingress controller instance for Citrix ADC CPX with the Citrix ingress controller as sidecar and Citrix ingress controller standalone deployments.

## Upgrade Citrix ADC CPX with Citrix ingress controller as a sidecar

To upgrade a Citrix ADC CPX with the Citrix ingress controller as a sidecar, you can either modify the associated YAML definition file (for example, [citrix-k8s-cpx-ingress.yml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/baremetal/citrix-k8s-cpx-ingress.yml)) or use the Helm chart.

If you want to upgrade by modifying the **YAML** definition file, perform the following:

1.  Change the version of the Citrix ingress controller and Citrix ADC CPX image under `containers` section to the following:
    -  Citrix ADC CPX version: 13.0-36.29 (`quay.io/citrix/citrix-k8s-cpx-ingress:13.0-36.29`)
    -  Citrix ingress controller version: 1.4.392 (`quay.io/citrix/citrix-k8s-ingress-controller:1.4.392`)
  
2.  Update the `CluterRole` as follows:

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

3.  Save the YAML definition file and reapply the file.

## Upgrade a standalone Citrix ingress controller to version 1.4.392

To upgrade a standalone Citrix ingress controller instance, you can either modify the **YAML** definition file or use the Helm chart.

If you want to upgrade Citrix ingress controller to version 1.4.392 by modifying the **YAML** definition file, perform the following:

1.  Change the version for the Citrix ingress controller image under `containers` section. For example, consider you have the following YAML file.

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
                image: "citrix-k8s-ingress-controller:1.4.392"
                env: ...
                args: ...

    You should change the version of the image to version 1.4.392. For example, `quay.io/citrix/citrix-k8s-ingress-controller:1.4.392`.

2.  Update the `ClusterRole` as follows:

        kind: ClusterRole
        apiVersion: rbac.authorization.k8s.io/v1beta1
        metadata:
          name: cic-k8s-role
        rules:
          - apiGroups: [""]
            resources: ["endpoints", "ingresses", "pods", "secrets", "nodes", "routes", "namespaces"]
            verbs: ["get", "list", "watch"]
          - apiGroups: [""]
            resources: ["services"]
            verbs: ["get", "list", "watch", "patch"]
          - apiGroups: ["extensions"]
            resources: ["ingresses", "ingresses/status"]
            verbs: ["get", "list", "watch"]
          - apiGroups: ["apiextensions.k8s.io"]
            resources: ["customresourcedefinitions"]
            verbs: ["get", "list", "watch"]
          - apiGroups: ["apps"]
            resources: ["deployments"]
            verbs: ["get", "list", "watch"]
          - apiGroups: ["citrix.com"]
            resources: ["rewritepolicies", "canarycrds", "authpolicies", "ratelimits"]
            verbs: ["get", "list", "watch"]
          - apiGroups: ["citrix.com"]
            resources: ["vips"]
            verbs: ["get", "list", "watch", "create", "delete"]
          - apiGroups: ["route.openshift.io"]
            resources: ["routes"]
            verbs: ["get", "list", "watch"]

3.  Save the YAML definition file and reapply the file.
