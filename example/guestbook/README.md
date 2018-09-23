# **Deploying Citrix Ingress Controller for Loadbalancing sample Guestbook App**
   Citrix ingress controller can be deployed as a pod inside K8’s cluster for configuring CITRIX MPX/VPX as ingress loadbalancer. 
   For CPX Citrix Ingress Controller runs as agent inside CPX pod.
   In this example, deploying a simple Guestbook web application and then configure load balancing for that application using the Ingress resource.
	

## **Guestbook**
   Guestbook is a simple, multi-tier PHP-based web application that uses redis chart.
   The guestbook application uses Redis to store its data. It writes its data to a Redis master instance and reads data from multiple Redis slave instances.
   Guesbook app details can be found [kubernetes.example](https://kubernetes.io/docs/tutorials/stateless-application/guestbook/)

## **Bring up the Application**
  Use following command to bringup guestbook application. Using `guestbook-all-in-one.yaml`, brings up frontend, redis master and slave application.   
  ```
    kubectl create -f guestbook-all-in-one.yaml
  ```
  Verify all the application is up and running by
  ```
   kubectl get pods --all-namespaces
  ```

## **Choose the  Deployment**

#### **1. Bring up Citrix Ingress Controller for VPX, MPX**
   Load balancing above application with  VPX/MPX which sits outside of kubernetes cluster requires citrix ingress controller and ingress resource.
   Deploy citrix ingress controller follow [Deployment](../../deployment)

   Update `guestbook-ingress.yml` with a valid virtual IP. Annotation for frontend ip is `ingress.citrix.com/frontend-ip`.

   ```
    kubectl create -f guestbook-ingress.yml
   ```
######  **Test The application**
    Create a "www.guestbook.com" domain name and update it with Virtual IP mentioned in the ingress resource. Access "www.guestbook.com" from url which opens guestbook application. 
       

#### **2. Bring up CPX with builtin Controller**

   Deploy CPX with citrix ingress controller follow [Deployment](../../deployment)
   Create an ingress resource by following command.
   ```
    kubectl create -f guestbook-ingress.yml
   ```

######  **Test The application**
   Create a "www.guestbook.com" domain name and update with service IP. Access "www.guestbook.com" from url which opens guestbook application. 
   
   Minikube users can use following command to get the service IP.
   ```
    minikube service cpx-service --url 
   ```
