# **Annotations**


List of annotations supported by Citrix Ingress Controller:

* ingress.citrix.com/frontend-ip 
```
            Custom VIP. This IP will be configured in NetScaler as VIP. 
            Default Value : NSIP of NetScaler.
```
* ingress.citrix.com/secure-port 
```
            Port for https traffic 
            This port will be configured in NetScaler CS Vserver. 
            Default Value : 443.
```
* ingress.citrix.com/insecure-port
```
            Port for http traffic 
            This port will be configured in NetScaler CS Vserver. 
            Default Value : 80.
```
* ingress.citrix.com/insecure-termination 
```
            Use "allow" to permit http traffic
            Use "redirect" to redirect http to https
            Use "disallow" to drop http traffic. 
            Default Value : disallow.
```
* ingress.citrix.com/secure-backend  
```
            Set secure-backend as True, to have SSL backend
            Default Value : False.
```


                        
