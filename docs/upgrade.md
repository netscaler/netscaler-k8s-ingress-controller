# Upgrade Netscaler ingress controller

This topic explains how to upgrade the Netscaler ingress controller instance for Netscaler CPX with the Netscaler ingress controller as sidecar and Netscaler ingress controller standalone deployments.

## Upgrade Netscaler CPX with Netscaler ingress controller as a sidecar

To upgrade a Netscaler CPX with the Netscaler ingress controller as a sidecar, you can either modify the associated YAML definition file (for example, [citrix-k8s-cpx-ingress.yml](https://github.com/netscaler/netscaler-k8s-ingress-controller/blob/master/deployment/baremetal/citrix-k8s-cpx-ingress.yml)) or use the Helm chart.

If you want to upgrade by modifying the **YAML** definition file, perform the following:

1.  Change the version of the Netscaler ingress controller and Netscaler CPX image under `containers` section to the following:
    -  Netscaler CPX version: 14.1-25.111 (`quay.io/netscaler/netscaler-cpx:14.1-47.48`)
    -  Netscaler ingress controller version: 2.1.4 (`quay.io/netscaler/netscaler-k8s-ingress-controller:3.3.2`)
  
2.  Update the `CluterRole` as follows:

        kind: ClusterRole
        apiVersion: rbac.authorization.k8s.io/v1
        metadata:
          name: cic-k8s-role
        rules:
          - apiGroups: [""]
            resources: ["endpoints", "ingresses", "services", "pods", "secrets", "nodes", "routes", "namespaces"]
            verbs: ["get", "list", "watch"]
          # services/status is needed to update the loadbalancer IP in service status for integrating
          # service of type LoadBalancer with external-dns
          - apiGroups: [""]
            resources: ["services/status"]
            verbs: ["patch"]
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
            verb s: ["get", "list", "watch", "create", "delete"]
          - apiGroups: ["route.openshift.io"]
            resources: ["routes"]
            verbs: ["get", "list", "watch"]

3.  Save the YAML definition file and reapply the file.

## Upgrade a standalone Netscaler ingress controller to version 1.5.25

To upgrade a standalone Netscaler ingress controller instance, you can either modify the **YAML** definition file or use the Helm chart.

If you want to upgrade Netscaler ingress controller to version 1.5.25 by modifying the **YAML** definition file, perform the following:

1.  Change the version for the Netscaler ingress controller image under `containers` section. For example, consider you have the following YAML file.

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
                image: "citrix-k8s-ingress-controller:1.5.25"
                env: ...
                args: ...

    You should change the version of the image to version 1.5.25. For example, `quay.io/netscaler/netscaler-k8s-ingress-controller:3.3.2`.

2.  Update the `ClusterRole` as follows:

        kind: ClusterRole
        apiVersion: rbac.authorization.k8s.io/v1
        metadata:
          name: cic-k8s-role
        rules:
          - apiGroups: [""]
            resources: ["endpoints", "ingresses", "pods", "secrets", "nodes", "routes", "namespaces"]
            verbs: ["get", "list", "watch"]
          # services/status is needed to update the loadbalancer IP in service status for integrating
          # service of type LoadBalancer with external-dns
          - apiGroups: [""]
            resources: ["services/status"]
            verbs: ["patch"]
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
