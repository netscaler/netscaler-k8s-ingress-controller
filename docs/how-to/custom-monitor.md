# **Creating custom monitor for the Application**

The topic covers how to create custom monitor for the application which would help to load balance the application better. Smart annnotation on Citrix Ingress Controller can be used for creating various types of Monitor for your applications. To configure monitors on a Web site, you first decide whether to use a built-in monitor or create your own monitor. If you create a monitor, you can choose between creating a monitor based on a built-in monitor, or creating a custom monitor that uses a script that you write to monitor the service. Once you have chosen or created a monitor, you can use smart annotation which creates the monitor and bound to the service. 
 

## **Smart annotation for monitor**

Anotation  created for monitor is ```ingress.citrix.com/monitor``` which can be used to create monitor of your choice. Citrix Ingress controller internally creates the monitor and bound to the right service.

For example:
```
ingress.citrix.com/monitor: '{"frontend":{"type":"http"}}'
```
In this example service called frontend is configured with default http monitor.


## **Choosing builtin Monitors**
  
  The NetScaler appliance contains a number of built-in monitors that you can use to monitor your services. These built-in monitors handle most of the common protocols. Based on the application you can choose the builtin monitor which suits your application. 
Here, we will show how we can use HTTP-Inline monitor the http application with help of smart annotation.


## **Configure a user monitor**

  To configure a user monitor, you must write a script that the monitor uses to check the services that are bound to it. Upload the script to the /nsconfig/monitors directory on the NetScaler appliance. Give executable permission to the script. If the monitor type is a protocol that the NetScaler appliance does not support, only then you must use the monitor of type USER.
Note: Monitor probes originate from the NSIP address. The scriptargs configured for the monitor of type USER is displayed in the running configuration and ns.conf files.
  Here we are using a user monitor for SFTP application. Name of the service used here is sftp and type of monitor is USER. Pasing the script ```nssftp.pl``` username and password as json input. 
  ![Monitor](../media/Monitor.png)
  Smaple ingress.
  ![Monitor](../media/Monitor_ingress.png)
  



