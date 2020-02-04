# **CPX HPA with Custom metrics**
## Kubernetes Autoscaling: Horizontal Pod Autoscaler(HPA)
* Horizontal Pod Autoscaler is a resource provided by Kubernetes which as the name implies, scales Kubernetes based resources like deployments, replica sets and replication controllers.
* Traditionally HPA gets its metrics from metrics-server. It then periodically adjusts the number of replicas in a deployment to match the observed average metrics to the target specified by user.

<p align="center">
<img src="images/image001.png" width="10000">
Figure 1. HPA with traditional metrics-server
</p>

## Why custom metrics for CPX?
By default, the metrics-server only gives us CPU and memory metrics for a pod. Both these metrics are neither very accurate nor very user-friendly with respect to a CPX (Citrix ADC) pod. So, we had to come up with our own custom metrics-server which would help us expose metrics like "HTTP requests rate" or "Bandwidth" from a CPX. 

## What needs to be done to achieve custom metrics for CPX?
We will be using Prometheus – which is a graduated CNCF project – to collect all the metrics from the CPX and exposing them using Prometheus-adapter which will be queried by the HPA controller to keep a check on the logs.
Prometheus-adapter contains an implementation of the Kubernetes resource metrics API and custom metrics API. This adapter is therefore suitable for use with the autoscaling/v2 Horizontal Pod Autoscaler in Kubernetes 1.6+. It can also replace the metrics server on clusters that already run Prometheus and collect the appropriate metrics.

Below, Figure 2, is a visual representation of how an HPA works. We have a 2-tier model with VPX which is load balancing the CPX deployment. The CPXs are in turn load balancing the applications. A Prometheus, Prometheus-adapter and an HPA controller for the CPX deployment are also deployed.
The HPA controller will keep polling the Prometheus-adapter for custom metrics like HTTP requests rate or Bandwidth. Whenever the limit defined by the user in the HPA is reached, it would scale the CPX deployment and create another CPX pod to handle the load.

<p align="center">
<img src="images/image002.png" width="1000">
Figure 2. Visual representation of CPX autoscaling with custom metrics from Prometheus-adapter
</p>

## To see CPX autoscaling in action follow the following steps:

### Step 1: Clone repo and change directory
Clone the citrix-k8s-ingress-controller repository from Github using the following command.

```git clone https://github.com/citrix/citrix-k8s-ingress-controller.git```

After cloning, go to the examples folder with the following command.

```cd citrix-k8s-ingress-controller/blob/master/example/hpa-demo/```

### Step 2: Set values for VPX

<img src="images/image003.png" width="500">

Open ```values.sh``` in the current directory and update the values on the right-hand side of ```VPX_IP```, ```VPX_PASSWORD``` and ```VIRTUAL_IP_VPX```. ```VPX_IP``` will be the IP of the VPX that we will be using. ```VPX_PASSWORD``` will be the password of the "nsroot" user on VPX. Finally, ```VIRTUAL_IP_VPX``` will be the IP on which we will be accessing the guestbook application. (This is a dummy application that we will be using for demo purposes.) 

### Step 3: Create all the resources
After the values.sh file is set. We can create all the resources by just running the ```create_all.sh``` file. This will create all the resources like Prometheus and Grafana for monitoring, CPX deployment, CIC pod for the VPX, ingress for both CPX and VPX, guestbook application and CPX HPA for monitoring the CPX deployment. Finally, we would also be installing a helm chart for exposing the custom metrics which is getting collected in the Prometheus.

Execute ```./create_all.sh```

### Step 4: Add an entry in the hosts file
We need to add a route in the hosts file in order to point http://www.guestbook.com application to the VPX Virtual IP that we had set in the 2nd step.
For most Linux distros, the ```hosts``` file is present in ```/etc``` folder.

### Step 5: Send traffic and see the CPX deployment autoscale
The CPX deployment HPA has been configured in such a way that when the average "HTTP requests rate" of the CPX goes above 20, it will autoscale.
There are two shell scripts in the folder. One for sending traffic below the threshold and one for sending traffic above the threshold. All this can be visualized in Grafana dashboard as shown in Figure 3 and Figure 5.

Run the ```16_curl.sh``` script to send 16 HTTP requests per second to the CPX. 

<p align="center">
<img src="images/image004.png" width="1000">
Figure 3. Grafana dashboard when 16 HTTP requests are sent per second.
</p>
<p align="center">
<img src="images/image005.png" width="1000">
Figure 4. HPA state with 16 RPS (requests per second)
</p>

Now, run the ```30_curl.sh``` script to send 30 requests per second to the CPX. In this we will see that the threshold of 20 that was set has been crossed and we will see that the CPX deployment has autoscaled from 1 pod to 2 pods. The average value of the metric "HTTP request rate" has also gone down from 30 to 15 in Figure 6 because there are 2 CPX pods now.
 
<p align="center">
<img src="images/image006.png" width="1000">
Figure 5. State of HPA when the average target is overshoot.
</p>
 
<p align="center">
<img src="images/image007.png" width="1000">
Figure 6. The number of replicas has gone up from 1 to 2 and the average is 15 RPS
</p>

<p align="center">
<img src="images/image008.png" alt="Figure 7. Grafana dashboard with 2 CPXs load balancing the traffic.">
Figure 7. Grafana dashboard with 2 CPXs load balancing the traffic.
</p>


### Step 6: Clean up
Now that we have seen HPA in action, we can clean up by just executing the ```delete_all.sh``` file.

Execute ```./delete_all.sh```
