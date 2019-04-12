# **Deploying Citrix Ingress Controller for Loadbalancing Guestbook App**

   Guestbook is a simple, multi-tier PHP-based web application that uses redis chart.
   The guestbook application uses Redis to store its data. It writes its data to a Redis master instance and reads data from multiple Redis slave instances.
   Guesbook app details can be found [kubernetes.example](https://kubernetes.io/docs/tutorials/stateless-application/guestbook/)

## **Bring up the application**
  Deploy frontend, redis master and slave micro services.   
  ```
    kubectl apply -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/example/guestbook/guestbook-all-in-one.yaml
  ```

## **Choose the  deployment**
#### **1. Bring up Citrix Ingress Controller for VPX, MPX**
######    1.1. Deploy Citrix ingress controller
   Follow [Deployment](../../docs/deploy) guide to deploy citrix ingress controller
######    1.2. Download the guestbook-ingress.yaml
   ```
   wget https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/example/guestbook/guestbook-ingress.yaml
   ```
######    1.3. Update the guestbook-ingress.yaml
   Update `guestbook-ingress.yaml` with a valid virtual IP. Annotation for frontend ip is `ingress.citrix.com/frontend-ip`.
######    1.4. Create the guestbook ingress
   ```
   kubectl create -f guestbook-ingress.yaml
   ```  
#### **2. Bring up CPX with builtin Controller**

######    2.1 Deploy CPX with citrix ingress controller
   Follow [Deployment](../../docs/deploy) guide to deploy the CPX with citrix ingress controller
######    2.2 Create an ingress resource by following command
   ```
    kubectl apply -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/example/guestbook/guestbook-ingress.yaml 
   ```

##  **Test the application**
   For CPX create a host entry for dns resolution`www.guestbook.com X.X.X.X(IP of k8s master node)` in hostfile.Get NodePort information for cpx-service(http)[kubectl describe service cpx-service].Access `http://www.guestbook.com:NodePort` from browser which opens guestbook application. 

For VPX create a host entry for dns resolution`www.guestbook.com X.X.X.X(frontend-ip in ingress.citrix.com/frontend-ip)` in hostfile..Access `http://www.guestbook.com` from browser which opens guestbook application. 

   Minikube users can use following command to get the service IP.
   ```
    minikube service cpx-service --url 
   ```
