# Ingress class support

## What is Ingress class?

In a Kubernetes cluster, there might be multiple ingress controllers and you need to have a way to associate a particular ingress resource with an ingress controller.

You can specify the ingress controller that should handle the ingress resource by using the `kubernetes.io/ingress.class` annotation in your ingress resource definition.

## Citrix ingress controller and Ingress classes

The Citrix ingress controller supports accepting multiple ingress resources, which have `kuberneters.io/ingress.class` annotation. Each ingress resource can be associated with only one `ingress.class`. However, the Ingress Controller might need to handle various ingress resources from different classes.

You can associate the Ingress Controller with multiple ingress classes using the `--ingress-classes` argument under the `spec` section of the YAML file.

If `ingress-classes` is not specified for the Ingress Controller, then it accepts all ingress resources irrespective of the presence of the `kubernetes.io/ingress.class` annotation in the ingress object.

If `ingress-classes` is specified, then the Ingress Controller accepts only those ingress resources that match the `kubernetes.io/ingress.class` annotation. The Ingress controller does not process an Ingress resource without the  `ingress.class` annotation in such a case.

!!! note "Note"
    Ingress class names are case-insensitive.

## Sample YAML configurations with Ingress classes

Following is the snippet from a sample YAML file to associate `ingress-classes` with the Ingress Controller. This configuration works in both cases where the Ingress Controller runs as a standalone pod or runs as a sidecar with Citrix ADC CPX. In the given YAML snippet, the following ingress classes are associated with the Ingress Controller.

-  `my-custom-class`

-  `Citrix`

```YAML
spec:
    serviceAccountName: cic-k8s-role
    containers:
    - name: cic-k8s-ingress-controller
      image:"quayio/citrix/citrix-k8s-ingress-controller:latest"
      # specify the ingress classes names to be supportedbyIngress Controller in args section.
      # First line should be --ingress-classes, andeverysubsequent line should be
      # the name of allowed ingress class. In the givenexampletwo classes named
      # "citrix" and "my-custom-class" are accepted. Thiswill be case-insensitive.
      args:
        - --ingress-classes
          Citrix
          my-custom-class
```

Following is the snippet from an Ingress YAML file where the Ingress class association is depicted. In the given example, an Ingress resource named `web-ingress` is associated with the ingress class `my-custom-class`. If the Citrix ingress controller is configured to accept `my-custom-class`, it processes this Ingress resource.

```yml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: web-ingress
  annotations:
     kubernetes.io/ingress.class: "my-custom-class"
```

## Updating the Ingress status for the Ingress resources with the specified IP address

To update the `Status.LoadBalancer.Ingress` field of the Ingress resources managed by the Citrix ingress controller with the allocated IP addresses, specify the command line argument `--update-ingress-status yes` when you start the Citrix ingress controller. This feature is only supported for the Citrix ingress controller deployed as a stand-alone pod for managing Citrix ADC VPX or MPX. For Citrix ADC CPXs deployed as sidecars, this feature is not supported.

Following is an example YAML with the  `--update-ingress-status yes` command line argument enabled.


```yml
apiVersion: v1
kind: Pod
metadata:
  name: cic-k8s-ingress-controller
spec:
  serviceAccountName: cic-k8s-role
  containers:
  - name: cic-k8s-ingress-controller
   image: "quay.io/citrix/citrix-k8s-ingress-controller:1.8.19"
env:
    # Set NetScaler NSIP/SNIP, SNIP in case of HA (mgmt has to be enabled)
    - name: "NS_IP"
      value: <Citrix ADC management IP>
    # Set username for Nitro
    - name: "NS_USER"
      valueFrom:
        secretKeyRef:
          name: nslogin
          key: username
    # Set user password for Nitro
    - name: "NS_PASSWORD"
      valueFrom:
        secretKeyRef:
          name: nslogin
          key: password
    - name: "EULA"
      value: "yes"
args:
    - --feature-node-watch false
    - --ipam citrix-ipam-controller
    - --update-ingress-status yes
    imagePullPolicy: Always
```

## Ingress status update for the sidecar deployment

In typical deployments, the Ingress status is updated with a public IP address or a host name of the Ingress controller after the ingress resource is successfully created and configured by the Ingress controller. The application that is exposed through the Ingress can be accessed through the public IP address or the host name that is updated in the Ingress status.

In cloud deployments, the Citrix ingress controller is exposed through a cloud load balancer. It is performed by creating a Kubernetes service type of `LoadBalancer`. In cloud deployments, the Ingress status is updated with the public endpoint of the cloud load balancer. The public endpoint can be an IP address or a host name depending on the public cloud.
This is applicable even on on-prem deployments. In dual-tier ingress deployments, in which the Citrix ADC CPX is exposed as service type `LoadBalancer` to the tier-1 Citrix ADC VPX ingress, the ingress resources operated by the Citrix ADC CPX is updated with the VIP address.

This topic provides information about how to enable the ingress status update for Citrix ADC CPX with the Citrix ingress controller as sidecar deployments.

**Note**:

The Ingress status update for the sidecar feature is supported only on services of type `LoadBalancer`.

**Sample Ingress output after an Ingress status update**

The following is a sample Ingress output after the Ingress status update:


        $ kubectl get ingress

        NAME             HOSTS              ADDRESS                           PORTS    AGE                                       
        sample-ingress   sample.citrix.com   sample.abc.somexampledomain.com   80      1d

## Enable Ingress status update for the sidecar deployments

You can enable the ingress status update feature by specifying the following argument in the Citrix ADC CPX YAML file. You must add the argument to the `args` section of Citrix ADC CPX in the deployment YAML file for Citrix ADC CPX with the Citrix ingress controller.


        args:
        - --cpx-service <namespace>/<name-of-the-service-exposing-cpx>

The following table describes the argument for the ingress update in detail

| Keyword/variable       | Description |
| ------------- |-------------|
| `--cpx-service` | Specifies the argument for enabling this feature. |
| `<namespace>/<name-of-the-service-exposing-cpx>`      | Specifies the format in which the argument value to be provided.      |
| `<namespace>` | Specifies the namespace in which the service is created. |
| `<name-of-the-service-exposing-cpx>` | Specifies the name of the service that exposes Citrix ADC CPX. |

**Note**:

The Ingress status update for the sidecar feature is supported only on services of type `LoadBalancer`. The service defined in the argument `--cpx-service default/some-cpx-service` should be a Kubernetes service of type=LoadBalancer.
