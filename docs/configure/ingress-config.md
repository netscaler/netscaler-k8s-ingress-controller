# Ingress configurations

Kubernetes [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) provides you a way to route requests to services based on the request host or path, centralizing a number of services into a single entry point.

Citrix ingress controller is built around Kubernetes Ingress and automatically configures one or more Citrix ADC based on the Ingress resource configuration.

## Host name based routing

The following sample Ingress definition demonstrates how to set up an Ingress to route the traffic based on the host name:

```yml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: Virtual-Host-Ingress
  namespace: default
spec:
  rules:
  - host: foo.bar.com
    http:
      paths:
      - backend:
          service:
            name: service1
            port:
              number: 80
        pathType: ImplementationSpecific
  - host: bar.foo.com
    http:
      paths:
      - backend:
          service:
            name: service2
            port:
              number: 80
        pathType: ImplementationSpecific
```

After the sample Ingress definition is deployed, all the HTTP request with a host header is load balanced by Citrix ADC to `service1`. And, the HTTP request with a host header is load balancer by Citrix ADC to `service2`.

## Path based routing

The following sample Ingress definition demonstrates how to set up an Ingress to route the traffic based on URL path:

```yml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: Path-Ingress
  namespace: default
spec:
  rules:
  - host: test.example.com
    http:
      paths:
      - backend:
          service:
            name: service1
            port:
              number: 80
        path: /foo
        pathType: ImplementationSpecific
      - backend:
          service:
            name: service2
            port:
              number: 80
        path: /
        pathType: ImplementationSpecific
```

After the sample Ingress definition is deployed, any HTTP requests with host `test.example.com` and URL path with prefix `/foo`, Citrix ADC routes the request to `service1` and all other requests are routed to `service2`.

Citrix ingress controller follows first match policy to evaluate paths. For effective matching, Citrix ingress controller orders the paths based on descending order of the path's length. It also orders the paths that belong to same hosts across multiple ingress resources.

## Wildcard host routing

The following sample Ingress definition demonstrates how to set up an ingress with wildcard host.

```yml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: Wildcard-Ingress
  namespace: default
spec:
  rules:
  - host: ’*.example.com’
    http:
      paths:
      - backend:
          service:
            name: service1
            port:
              number: 80
        path: /
        pathType: ImplementationSpecific
```

After the sample Ingress definition is deployed, HTTP requests to all the subdomains of `example.com` is routed to `service1` by Citrix ADC.

>**Note:**
> Rules with non-wildcard hosts are given higher priority than wildcard hosts. Among different wildcard hosts, rules are ordered on the descending order of length of hosts.

## Exact path matching

By default Ingress paths are treated as prefix expressions. Using the annotation `ingress.citrix.com/path-match-method: “exact”` in the ingress definition defines the Citrix ingress controller to consider the path for the exact match.

The following sample Ingress definition demonstrates how to set up Ingress for exact path matching:

```yml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    ingress.citrix.com/path-match-method: “exact”
  name: Path-exact-Ingress
  namespace: default
spec:
  rules:
  - host: test.example.com
    http:
      paths:
      - backend:
          service:
            name: service1
            port:
              name: "80"
        path: /exact
        pathType: ImplementationSpecific
```

After the sample Ingress definition is deployed, HTTP requests with path `/exact` is routed by Citrix ADC to `service1` but not to `/exact/somepath`.

## Non-Hostname routing

Following example shows path based routing for the default traffic that does not match any host based routes. This ingress rule applies to all inbound HTTP traffic through the specified IP address.

```yml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: Default-Path-Ingress
  namespace: default
spec:
  rules:
  - http:
      paths:
      - backend:
          service:
            name: service1
            port:
              number: 80
        path: /foo
        pathType: ImplementationSpecific
      - backend:
          service:
            name: service2
            port:
              number: 80
        path: /
        pathType: ImplementationSpecific
```

All incoming traffic that does not match the ingress rules with host name is matched here for the paths for routing.

## Default back end

Default back end is a service that handles all traffic that is not matched against any of the Ingress rules.

```yml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: Default-Ingress
  namespace: default
spec:
  defaultBackend:
    service:
      name: testsvc
      port:
        number: 80

```

>**Note:**
> A global default back end can be specified if Citrix ADC CPX is load balancing the traffic. You can create a default back end per `frontend-ip:port` combination in case of Citrix ADC VPX or MPX is the ingress device.
