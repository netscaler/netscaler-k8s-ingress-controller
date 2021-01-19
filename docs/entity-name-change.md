# Entity name change

While adding the Citrix ADC entities, the Citrix ingress controller maintains unique names per Ingress, service or namespace. Sometimes, it results in Citrix ADC entities with large names even exceeding the name limits in Citrix ADC.

Now, the naming format in the Citrix ingress controller is updated to shorten the entity names. In the updated naming format, a part of the entity name is hashed and all the necessary information is provided as part of the entity comments.

After this update, the comments available on `lbvserver` and `servicegroup` entity names provides all the necessary details like the ingress name, ingress port, service name, service port, and the namespace of the application.

**Format for comments**

Ingress: `ing:<ingress-name>,ingport:<ingress-port>,ns:<k8s-namespace>,svc:<k8s-servicename>,svcport:<k8s-serviceport>`

Service of `type LoadBalancer`: `lbsvc:<k8s-servicename>,svcport:<k8s-serviceport>,ns:<k8s-namespace>`


The following table explains the entity name changes introduced with the Citrix ingress controller version 1.12.

| Entity | Old naming format | New naming format | Description/Comments   |
| ------------------------ | ---------- | --------------------------- | ------|
| `csvserver` (ingress)|`k8s-192.2.170.67_80_http`  |`k8s-192.2.170.67_80_http`  |  no changes|
| `csvserver` (`type LoadBalancer`) | `k8s-apache_default_80_svc` | `k8s-apache_80_default_svc` | Now, the port is followed by a namespace |
| `lbvserver` (`type LoadBalancer`) | `k8s-apache_default_80_svc_k8s-apache_default_80_svc`| `k8s-apache_80_lbv_wlikeqxno5vunbthsoj4lxegk7cddh6p` Comment: `lbsvc:apache,svcport:80,ns:default`| The comment for `type LoadBalancer` is now different |
| `servicegroup` (`type LoadBalancer`) | `k8s-apache_default_80_svc_k8s-apache_default_80_svc` | `k8s-apache_80_sgp_wlikeqxno5vunbthsoj4lxegk7cddh6p` |The suffix `sgp` is added  |
| `cspolicy` or `csaction` or `responder policy`| `k8s-web-ingress_default_443_k8s-frontend_default_80_svc` | `k8s-frontend_80_csp_267pneiak5rw6hoygvrqrzpm4k6thz2p` | Moved service-name, service-port to the beginning, added suffix of cs, hashed ingress-name, ingress-port, and namespace |
| `lbvserver` (ingress)| `k8s-web-ingress_default_443_k8s-frontend_default_80_svc` | `k8s-frontend_80_lbv_267pneiak5rw6hoygvrqrzpm4k6thz2p` Comment: `ing:web-ingress,ingport:5080,ns:default,svc:frontend,svcport:80` | Suffix `lbv` and comment added to the entity |
| `servicegroup` (ingress)| `k8s-web-ingress_default_443_k8s-frontend_default_80_svc` | `k8s-frontend_80_sgp_267pneiak5rw6hoygvrqrzpm4k6thz2p` | Suffix `sgp` is added. |
| `lbvserver` (UDP)| `k8s-web-ingress_default_9053-udp_k8s-bind_default_53-udp_svc` | `k8s-bind_53-udp_lbv_uyomblblagixrtw3cxrf23tak6wkpfmw` | `-udp` is still appended to the port as earlier.|

When you upgrade from an older version of the Citrix ingress controller to the latest version, the Citrix ingress controller renames all the entities with the new naming format. However, the Citrix ingress controller does not handle the downgrade from the latest version to an older version.