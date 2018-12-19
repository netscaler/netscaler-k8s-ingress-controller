# Smart Annotations

Annotations are used for configuring the ingress devices in kubernetes. However the number of features and configuration elements at ingress devices are huge which leads to  very large number of annotation requirements.

Smart annotation is a method of enabling NetScaler features efficiently by using entity name. Ingress in kubernetes convert to set of NetScaler objects by Citrix Ingress Controller which can be control by using Smart annotations. Smart annotation takes Json format input and its key and value should match with NetScaler nitro format.<br/> 
Example, for enabling SRCIPDESTIPHASH based lb method, one must use corresponding Nitro key and value format "lbmethod" ,"SRCIPDESTIPHASH" respectively.



## List of Smart Annotations

Following smart annotations are available.<br/>
1. csvserver<br/>
   ```
   ingress.citrix.com/csvserver:
   ```
   This allows enables or set  all the cs vserver level entity configurations.
   ```
   example:
           ingress.citrix.com/csvserver: '{"soPersistence": "eNABLED", "precedence": "URL"}'
   ```        
   
2. lbvserver<br/>
   ```
   ingress.citrix.com/lbvserver
   ```
   ```
   example:
          ingress.citrix.com/lbvserver: '{"nginx-svc":{"lbmethod":"SRCIPDESTIPHASH"}}'
   ```
3. servicegroup
   ```
   ingress.citrix.com/servicegroup
   ```
   ```
   example: 
           ingress.citrix.com/servicegroup: '{"frontend":{"cip": "Enabled","cipHeader":"X-Forwarded-For"}}'
   ```
4. monitor
   ```
   ingress.citrix.com/monitor
   ```
   ```
   example:
          ingress.citrix.com/monitor: '{"frontend":{"type":"http"}}'
   ```
   
   
  
## Syntax of Smart annotations

   Smart annotations maps user inputs to NetScaler Configurations hence user has to make sure that json format they use is correct. make sure the inputs 'key' and 'value' are matching with nitro format.
   Smart annotations simply fine tune the application configuration, even if by chance input is wrong that alone will not get apply. There will be error notification for such failure.
   
## Sample Ingress yaml and Smart annotations

Here is sample ingress yaml and set of smart annotation use cases. service used here is nginx-svc which is refered in smart annotations.
```
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: nginx
  annotations:
    NETSCALER_HTTP_PORT: "80"
    NETSCALER_VIP: "192.168.1.1"
    ingress.citrix.com/csvserver: '{"l2conn":"on"}'
    ingress.citrix.com/lbvserver: '{"nginx-svc":{"lbmethod":"SRCIPDESTIPHASH"}}'
    ingress.citrix.com/servicegroup: '{"nginx-svc":{"usip":"yes"}}'
    ingress.citrix.com/monitor: '{"nginx-svc":{"type":"http"}}'
spec:
  rules:
  - host:  nginx.org
    http:
      paths:
      - path: /
        backend:
          serviceName: nginx-svc
          servicePort: 80
```          
          
          
          
