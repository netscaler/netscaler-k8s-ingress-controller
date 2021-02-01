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

## Ingress V1 and IngressClass support

With the Kubernetes version 1.19, the Ingress resource is generally available.
As a part of this change, a new resource named as `IngressClass` is added to the ingress API. Using this resource, you can associate specific Ingress controllers to Ingresses. For more information on the `IngressClass` resource, see the [Kubernetes documentation](https://kubernetes.io/docs/concepts/services-networking/ingress/#ingress-class).

The following is a sample `IngressClass` resource.

```yml

apiVersion: networking.k8s.io/v1
kind: IngressClass
metadata:
  name: citrix
spec:
  controller: citrix.com/ingress-controller

```

An `IngressClass`resource must refer to the ingress class associated with the controller that should implement the Ingress rules as shown as follows:

```yml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: minimal-ingress
spec:
  ingressClassName: citrix
  host: abc.com
  rules:
  - http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: test
            port:
              number: 80
```

The Citrix ingress controller uses the following rules to match the Ingresses.

- If the Citrix ingress controller is started without specifying the `--ingress-classes` argument 
   - If the Kubernetes version is lesser than 1.19 (IngressClass V1 resource is supported)
      - Matches any ingress object

   - If the Kubernetes version is greater than or equal to 1.19 (IngressClass V1 resource is supported)
     - Matches any ingress object in which the `spec.ingressClassName` field is not set.
   - Matches any ingress if the `spec.ingressClassName` field of the Ingress object is set and a `v1.IngressClass` resource exists with the same name and the `spec.controller` field of the resource is `citrix.com/ingress-controller`.

- If the Citrix ingress controller is started with one or more ingress classes set using the `--ingress-classes` argument.

  - If the Kubernetes version is lesser than 1.19 (IngressClass V1 resource is supported)
    - Matches any ingress with the ingress class annotation `kubernetes.io/ingress.class `matching to that of the configured ingress classes.
  - If the Kubernetes version is greater than or equal to 1.19 (IngressClass V1 resource is supported)
     - Matches any ingress in which the ingress class annotation `kubernetes.io/ingress.class` matches with the configured ingress classes. This annotation is deprecated but it has higher precedence over the `spec.IngressClassName` field to support backward compatibility.
     - Matches any ingress object, if a `v1.IngressClass` resource exists with the following attributes:
       - The name of the resource matches the `--ingress-classes` argument value.
       - The `spec.controller` field of the resource is set as the `citrix.com/ingress-controller`.
       -  The name of the resource matches with the `spec.ingressClassName` field of the Ingress object.
     - Matches any ingress object where the `spec.ingressClassName` field is not set and if a `v1.IngressClass` resource exists with the following attributes: 
       - The name of the resources matches the `--ingress-classes` argument value.
       - The `spec.controller` field of the resource is set as `citrix.com/ingress-controller`.
       - The resource is configured as the default class using the `ingressclass.kubernetes.io/is-default-class` annotation. For more information, see the [Kubernetes documentation](https://kubernetes.io/docs/concepts/services-networking/ingress/#default-ingress-class).

**Note:** If both the annotation and `spec.ingressClassName` is defined, the annotation is matched before the `spec.ingressClassName`. If the annotation does not match, the matching operation for the `spec.ingressClassName` field is not performed.

**Note:** When you are using Helm charts to install the Citrix ingress controller, if the `IngressClass` resource is supported and the Citrix ingress controller is deployed with the `--ingress-classes` argument, the `v1.IngressClass` resource is created by default.

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

## Ingress status update for sidecar deployments

In Kubernetes, Ingress can be used as a single entry point for exposing multiple applications to the outside world. The Ingress would have an `Address` (`Status.LoadBalancer.IP`) field which is updated after the successful ingress creation. This field is updated with a public IP address or host name through which the Kubernetes application can be reached. In cloud deployments, this field can also be the IP address or host name of a cloud load-balancer.

In cloud deployments, Citrix ADC CPX along with the ingress controller is exposed using a service of `type LoadBalancer` which in turn creates a cloud load-balancer. The cloud load balancer then exposes the Citrix ADC CPX along with the ingress controller. So, the Ingress resources exposed with the Citrix ADC CPX should be updated using the public IP address or host name of the cloud load balancer.

This is applicable even on on-prem deployments. In dual-tier ingress deployments, in which the Citrix ADC CPX is exposed as service type `LoadBalancer` to the tier-1 Citrix ADC VPX ingress, the ingress resources operated by the Citrix ADC CPX is updated with the VIP address.

This topic provides information about how to enable the ingress status update for Citrix ADC CPX with the Citrix ingress controller as sidecar deployments.

**Note**:

The ingress status update for the sidecar feature is supported only on services of type `LoadBalancer`.

**Sample ingress output after an ingress status update**

The following is a sample ingress output after the ingress status update:


        $ kubectl get ingress

        NAME             HOSTS              ADDRESS                           PORTS    AGE                                       
        sample-ingress   sample.citrix.com   sample.abc.somexampledomain.com   80      1d

## Enable ingress status update for the sidecar deployments

You can enable the ingress status update feature for side car deployments by specifying the following argument in the Citrix ADC CPX YAML file. You must add the argument to the `args` section of Citrix ADC CPX in the deployment YAML file for Citrix ADC CPX with the Citrix ingress controller.

       

        args:
        - --cpx-service <namespace>/<name-of-the-type-load-balancer-service-exposing-cpx>

The following table describes the argument for the ingress update in detail

| Keyword/variable       | Description |
| ------------- |-------------|
| `--cpx-service` | Specifies the argument for enabling this feature. |
| `<namespace>/<name-of-the-type-load-balancer-service-exposing-cpx>`      | Specifies the format in which the argument value to be provided.      |
| `<namespace>` | Specifies the namespace in which the service is created. |
| `<name-of-the-type-load-balancer-service-exposing-cpx>` | Specifies the name of the service that exposes Citrix ADC CPX. |

**Note**:

The ingress status update for the sidecar feature is supported only on services of type `LoadBalancer`. The service defined in the argument `--cpx-service default/some-cpx-service` should be a Kubernetes service of `type LoadBalancer`.