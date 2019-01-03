# Citrix Ingress Controller user command policy for VPX/MPX 

In order for Citrix Ingress Controller to configure a Tier-1 VPX/MPX, we would need to provide a system user of VPX/MPX that has certain privileges. This guide explains the privileges required and the configuration that is to be done in VPX/MPX for that.

## Permissions required by Citrix Ingress Controller:

* configure (add/delete/view) CS vServer
* configure CS policies and actions
* configure LB vServer
* configure Service groups
* configure SSL cert Keys
* configure routes
* configure user monitors
* add system file (for uploading SSL certkeys from Kubernetes)
* show ns ip (to configure a VIP)
* stat system (to check if VPX is UP)

## Citrix ADC's Configuration:

Configure the below commands in the Citrix ADC CLI

```
add system user cic citrix123
add cmdpolicy cic-policy ALLOW "(^\S+\s+cs\s+\S+)|(^\S+\s+lb\s+\S+)|(^\S+\s+service\s+\S+)|(^\S+\s+servicegroup\s+\S+)|(^stat\s+system)|(^show\s+ha)|(^\S+\s+ssl\s+certKey)|(^\S+\s+ssl)|(^\S+\s+route)|(^\S+\s+monitor)|(^show\s+ns\s+ip)|(^\S+\s+system\s+file)"
bind system user cic cic-policy 0
```

Now this user can be specified in the Citrix Ingress Controller yaml file in place of `NS_USER` and `NS_PASSWORD`


```
- name: "NS_USER"
  value: "cic"
# Set user password for Nitro
- name: "NS_PASSWORD"
  value: "citrix123"
```

Please note that the username and password are specified for illustration only. Please change this according to your needs.