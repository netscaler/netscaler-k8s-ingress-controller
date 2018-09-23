# **Deploying Citrix Ingress Controller for Loadbalancing Guestbook App**

   Guestbook is a simple, multi-tier PHP-based web application that uses redis chart.
   The guestbook application uses Redis to store its data. It writes its data to a Redis master instance and reads data from multiple Redis slave instances.
   Guesbook app details can be found [kubernetes.example](https://kubernetes.io/docs/tutorials/stateless-application/guestbook/)

## **Bring up the Application**
  Deploy frontend, redis master and slave micro services.   
  ```
    kubectl create -f guestbook-all-in-one.yaml
  ```

## **Choose the  Deployment**

#### **1. Bring up Citrix Ingress Controller for VPX, MPX**
   Deploy Citrix ingress controller follow [Deployment](../../deployment).

   Update `guestbook-ingress.yml` with a valid virtual IP. Annotation for frontend ip is `ingress.citrix.com/frontend-ip`.

   ```
    kubectl create -f guestbook-ingress.yml
   ```

#### **2. Bring up CPX with builtin Controller**

   Deploy CPX with citrix ingress controller follow [Deployment](../../deployment).
   Create an ingress resource by following command.
   ```
    kubectl create -f guestbook-ingress.yml
   ```
##  **Test The application**
   Create a "www.guestbook.com" domain name and update with NodePort IP of cpx-service(CPX)/Vserver IP(VPX/MPX).
   Access "www.guestbook.com" from url which opens guestbook application. 
   
   Minikube users can use following command to get the service IP.
   ```
    minikube service cpx-service --url 
   ```
