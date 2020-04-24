# **Creating monitor for the Application**
	
The topic covers how to create a monitor for the application which would help to load balance the application better. Citrix ADC supports two types of monitors.

1. Built-in Monitors
2. Custom Monitors

Smart annotation on Citrix Ingress Controller can be used for creating various types of monitor for your applications. you can choose between creating a monitor based on a built-in monitor, or creating a custom monitor that uses a script that you write to monitor the service. Once you have chosen or created a monitor, you can use smart annotation which manages the monitor lifecycle for your application. 
 

## **Smart annotation for monitor**

Annotation used for monitor is ```ingress.citrix.com/monitor``` which can be used to create monitor of your choice. Citrix Ingress controller internally creates the monitor and bound to the right service.



## **Configure a built-in Monitor**
  
The Citrix ADC appliance contains a number of built-in monitors that you can use to monitor your services. These built-in monitors handle most of the common protocols. Based on the application you can choose the built-in monitor which suits your application. 

Here is an example of using  HTTP monitor with the help of smart annotation.

```
ingress.citrix.com/monitor: '{"frontend":{"type":"http", "httpRequest":"GET /", "respcode":"200", "retries":"2"}}'
```

In this example,  service called ```frontend``` is configured with http monitor wicth send a GET request for which expect 200 response. When Citrix ingress controller gets this event, it creates a monitor and bind with the corresponding service of frontend.

  Sample ingress.

  ![HttpInline](../media/Http.png)

  Coresponding ADC Configurations.

  ![HttpInlineADC](../media/HttpOutput.png)

## **Configure a user monitor**

In addition to built-in monitors, you can use custom monitors to check the state of your services. The NetScaler appliance provides several types of custom monitors based on scripts that are included with the NetScaler operating system that can be used to determine the state of services based on the load on the service or network traffic sent to the service. These are the inline monitors, user monitors, and load monitors. With any of these types of monitors, you can use the supplied functionality, or you can create your own scripts and use those scripts to determine the state of the service to which the monitor is bound. Following are already provided scripts.

  ![CustomMonitor](../media/CustomMonitor.png)

  Here we are using a user monitor for SFTP application. Name of the service used here is sftp and type of monitor is USER. Providing the script ```nssftp.pl``` which is already available in ADC.

  ```
    ingress.citrix.com/monitor: '{"sftp":{"type":"USER", "scriptname":"nssftp.pl", "scriptargs":"file=/sftp/incoming/test.log;user=admin;password=admin"}}'
  ```  

  Sample ingress.

  ![MonitorIngress](../media/Monitor_ingress.png)
  
  When this ingress applied for the service sftp, a user monitor will be created on Citrix ADC and bound to the service.  
 
  Coresponding ADC Configurations.

  ![MonitorConfig](../media/MonitorOutput.png)


