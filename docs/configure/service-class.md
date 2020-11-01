# Service class for services of type LoadBalancer

When services of type LoadBalancer are deployed, all such services are processed by the Citrix ingress controller and configured on Citrix ADCs. However, there may be situations where you want to associate only specific services to a Citrix ingress controller if multiple Ingress controllers are deployed.
For Ingress resources this functionality is already available using the [Ingress class](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/configure/ingress-classes/) feature. Similar to the Ingress class functionality for Ingress resources, service class functionality is now added for services of type `LoadBalancer`.

You can associate a Citrix ingress controller with multiple service classes using the `--service-classes` argument under the `spec` section of the YAML file. If a service class is not specified for the ingress controller, then it accepts all services of the type `LoadBalancer` irrespective of the presence of the `service.citrix.com/class` annotation in the service.
If the service class is specified to the Citrix ingress controller, then it accepts only those services of the type `LoadBalancer` that match the `service.citrix.com/class` annotation. In this case, the Citrix ingress controller does not process a type `LoadBalancer` service if it is not associated with the `service.citrix.com/class` annotation.

## Sample YAML configurations with service classes

Following is a snippet from a sample YAML file to associate `service-classes` with the Ingress Controller. In this snippet, the following service classes are associated with the Ingress Controller.

-  `svc-class1`
-  `svc-class2`

```YAML

spec:
serviceAccountName: cic-k8s-role
containers:
- name: cic-k8s-ingress-controller
  # specify the service classes to be supported by Citrix Ingress Controller in args section.
  # First line should be --service-classes, and every subsequent line should be
  # the name of allowed service class. In the given example two classes named
  # "svc-class1" and "svc-class2" are accepted. This will be case-insensitive.
  args:
    - --service-classes
      svc-class1
      svc-class2
```

Following is a snippet from a type LoadBalancer service definition YAML file where the service class association is depicted. In this example, an Apache service is associated with the service class `svc-class1`. If the Citrix ingress controller is configured to accept `svc-class1`, it configures the service on the Citrix ADC.


```yml
apiVersion: v1
kind: Service
metadata:
     name: apache
     annotations:
         service.citrix.com/class: 'svc-class1'
     labels:
        name: apache
spec:
   type: LoadBalancer
   selector:
       name: apache
   ports:
   - name: http
     port: 80
     targetPort: http
   selector:
   app: apache
```
