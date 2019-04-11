# Upgrading Citrix Ingress Controller

This topic explains how to upgrade the Citrix Ingress Controller (CIC) instance for Citrix ADC CPX with CIC as sidecar and CIC standalone deployments.

## Upgrading Citrix ADC CPX with CIC as Sidecar

To upgrade a Citrix ADC CPX instance with CIC as sidecar, you can follow the procedure available at: [Upgrading a NetScaler CPX Instance](https://docs.citrix.com/en-us/citrix-adc-cpx/12-1/upgrade-cpx.html).

## Upgrading a Standalone CIC

To upgrade a standalone CIC instance, you can either modify the YAML definition file or use the Helm chart. In the YAML file, you need to change the version for the image under containers. For example, consider you have the following YAML file.

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
        image: "quay.io/citrix/citrix-k8s-ingress-controller:0.1.0"
        env: ...
        args: ...

```

You should change the version of the image to the required version. For example, `quay.io/citrix/citrix-k8s-ingress-controller:0.18.0`.

After updating the YAML file, you can use one of the following ways to upgrade the CIC image:

- Using the `kubectl edit` command, type `kubectl edit Deployment cic-k8s-ingress-controller`.
    This command enables you to upgrade the CIC image after you save the changes.

- Using the `kubectl set` command, type `kubectl set image Deployment/cic-k8s-ingress-controller  cic-k8s-ingress-controller=quay.io/citrix/citrix-k8s-ingress-controller:0.18.0`
    This command enables you to upgrade the CIC image.