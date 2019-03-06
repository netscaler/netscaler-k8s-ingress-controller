# Ingress Class Support

### Need for Ingress Class

In Kubernetes cluster, there might be multiple ingress controllers, and one needs to have a way to associate a particular ingress resource with an ingress controller.
_kubernetes.io/ingress.class_ annotation in the ingress resource enables multiple ingress controllers to run effectively in the cluster. Otherwise every ingress resource will be processed by all ingress controllers in the cluster.

### Citrix Ingress Controller and Ingress classes

Citrix Ingress Controller provides a support to accept multiple ingress resources which have _kuberneters.io/ingress.class_ annotations. Each ingress resource can be associated with only one ingress.class,
however Ingress Controller might need to handle various ingress resources from different classes.

Ingress Controller can be associated with multiple ingress classes using *_'--ingress-classes'_* argument under spec section of the yaml file.

If ingress-classes are not specified for Ingress Controller, then it accepts all ingress resources irrespective the presence of _kubernetes.io/ingress.class_ annotation in ingress object.
If ingress-classes are specified, then Ingress Controller accepts only those ingress resources for which _kubernetes.io/ingress.class_ annotation matches. Please note that ingress resource without ingress.class annotation will not be handled by Ingress Controller in the given case.

**Note:** Ingress class names are case-insensitive

### Sample yaml configurations with ingress-classes 
Below is the snippet from sample yaml files to associate ingress-classes with the Ingress Controller. This works in both cases where Ingress Controller runs as a standalone pod or runs along with CPX proxy.
In given yaml snippet, two ingress classes are associated with Ingress Controller
  1) my-custom-class
  2) Citrix.

```yaml
spec:
      serviceAccountName: cic-k8s-role
      containers:
      - name: cic-k8s-ingress-controller
        image: "quay.io/citrix/citrix-k8s-ingress-controller:1.1.1"
        # specify the ingress classes names to be supported by Ingress Controller in args section.
        # First line should be --ingress-classes, and every subsequent line should be
        # the name of allowed ingress class. In the given example two classes named
        # "citrix" and "my-custom-class" are accepted. This will be case-insensitive.
        args:
          - --ingress-classes
            Citrix
            my-custom-class
```

Below is the snippet of Ingress yaml file where Ingress class association is depicted.
In the given example, Ingress resource named _web-ingress_ is associated with the ingress class _my-custom-class_.
If Citrix Ingress Controller is configured to accept _my-custom-class_, it will process this Ingress resource.

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: web-ingress
  annotations:
     kubernetes.io/ingress.class: "my-custom-class"
```
