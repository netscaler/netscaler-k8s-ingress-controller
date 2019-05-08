# Expose services using NodePort

The Ingress Citrix ADC (VPX, MPX, or CPX) outside the Kubernetes cluster receives all the Ingress traffic to the microservices deployed in the Kubernetes cluster. You need to establish network connectivity between the Ingress Citrix ADC instance and the pods for the ingress traffic to reach the microservices.

As the pods run on overlay network, the pod IP addresses are private IP addresses and the Ingress Citrix ADC instance cannot reach the microservices running within the pods. To make the service accessible from outside of the cluster, you can create the service of type [NodePort](https://kubernetes.io/docs/concepts/services-networking/service/#nodeport). In your service definition file, specify `spec.type:NodePort` and optionally specify a port in the 30000–32767 as shown in the following sample:

```yaml
apiVersion: apps/v1beta2
kind: Deployment
metadata:
  name: apache
  labels:
      name: apache
spec:
  selector:
    matchLabels:
      app: apache
  replicas: 8
  template:
    metadata:
      labels:
        app: apache
    spec:
      containers:
      - name: apache
        image: httpd:latest
        ports:
        - name: http
          containerPort: 80
        imagePullPolicy: IfNotPresent
---
#Expose the apache web server as a Service
apiVersion: v1
kind: Service
metadata:
  name: apache
  annotations:  
    service.citrix.com/managed-service: "false"
  labels:
    name: apache
spec:
  type: NodePort
  selector:
    name: apache
  ports:
  - name: http
    port: 80
    targetPort: http
  selector:
    app: apache
```

The sample deploys and exposes the apache web server as a service. You can access the service using the `<NodeIP>:<NodePort>` address.