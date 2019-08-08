# Expose Service of type NodePort using Ingress

In a single-tier deployment, the Ingress Citrix ADC (VPX or MPX) outside the Kubernetes cluster receives all the Ingress traffic to the microservices deployed in the Kubernetes cluster. You need to establish network connectivity between the Ingress Citrix ADC instance and the pods for the ingress traffic to reach the microservices.

As the pods run on overlay network, the pod IP addresses are private IP addresses and the Ingress Citrix ADC instance cannot reach the microservices running within the pods. To make the service accessible from outside of the cluster, you can create the service of type [NodePort](https://kubernetes.io/docs/concepts/services-networking/service/#nodeport). The Citrix ADC instance load balances the Ingress traffic to the nodes that contain the pods.

To create the service of type [NodePort](https://kubernetes.io/docs/concepts/services-networking/service/#nodeport), in your service definition file, specify `spec.type:NodePort` and optionally specify a port in the range 30000–32767.

## Sample deployment

In this section, we shall create a Deployment, `apache`, and deploy it in your Kubernetes cluster. The following is a manifest for the Deployment:

```yaml
# If using this on GKE
# Make sure you have cluster-admin role for your account
# kubectl create clusterrolebinding citrix-cluster-admin --clusterrole=cluster-admin --user=<username of your google account>
#

#For illustration a basic apache web server is used as a application
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
```

The containers in this Deployment listen on port 80.

Copy the manifest to a file named `apache-deployment.yaml` and create the Deployment using the following command:

    kubectl create -f apache-deployment.yaml

Verify that eight Pods are running using the following:

    kubectl get pods

Once you verify the Pods are up and running, create a service of type `NodePort`. The following is a manifest for the service:

```yml
#Expose the apache web server as a Service
apiVersion: v1
kind: Service
metadata:
  name: apache
  labels:
    name: apache
spec:
  type: NodePort
  ports:
  - name: http
    port: 80
    targetPort: http
  selector:
    app: apache
```

Copy the manifest to a file named `apache-service.yaml` and create the service using the following command:

    kubectl create -f apache-service.yaml

The sample deploys and exposes the apache web server as a service. You can access the service using the `<NodeIP>:<NodePort>` address.
