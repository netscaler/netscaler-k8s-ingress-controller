# Ingress class support

## What is Ingress Class?

In Kubernetes cluster, there might be multiple ingress controllers, and you need to have a way to associate a particular ingress resource with an ingress controller. `kubernetes.io/ingress.class` annotation in the ingress resource enables multiple ingress controllers to run effectively in the cluster. Otherwise every ingress resource is processed by all the ingress controllers in the cluster.

## Citrix Ingress Controller and Ingress classes

Citrix Ingress Controller provides a support to accept multiple ingress resources, which have `kuberneters.io/ingress.class` annotation. Each ingress resource can be associated with only one `ingress.class`. However Ingress Controller might need to handle various ingress resources from different classes.

You can associate Ingress Controller with multiple ingress classes using `--ingress-classes` argument under spec section of the YAML file.

If ingress-classes are not specified for Ingress Controller, then it accepts all ingress resources irrespective of the presence of `kubernetes.io/ingress.class` annotation in the ingress object. If `ingress-classes` are specified, then Ingress Controller accepts only those ingress resources for which match the `kubernetes.io/ingress.class` annotation. Ingress resource without `ingress.class` annotation is not handled by Ingress Controller in the given case.

!!! note "Note"
    Ingress class names are case-insensitive.

## Sample yaml configurations with ingress-classes

Following is the snippet from a sample yaml file to associate `ingress-classes` with the Ingress Controller. This works in both cases where Ingress Controller runs as a standalone pod or runs as sidecar with Citrix ADC CPX. In the given yaml snippet, following ingress classes are associated with the Ingress Controller.

-  my-custom-class

-  Citrix

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

Following is the snippet from an Ingress yaml file where Ingress class association is depicted. In the given example, Ingress resource named `web-ingress` is associated with the ingress class `my-custom-class`. If Citrix Ingress Controller is configured to accept `my-custom-class`, it processes this Ingress resource.

```yml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: web-ingress
  annotations:
     kubernetes.io/ingress.class: "my-custom-class"
```