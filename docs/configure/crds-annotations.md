# Apply CRDs through annotations

You can now apply CRDs such as Rewrite and Responder, Ratelimit, Auth, WAF, and Bot for ingress resources and services of type load balancer by referring them using annotations. Using this feature, when there are multiple services in an Ingress resource, you can apply the rewrite and responder policy for a specific service or all the services based on your requirements.

The following are the two benefits of this feature:

-  You can apply a CRD at a per-ingress, per-service level. For example, the same service referred through an internal VIP may have different set of rewrite-responder policies compared to the one exposed outside.
-  Operations team can create CRD instances without specifying the service names. The application developers can choose the right policies based on their requirements.

**Note:** CRD instances should be created without service names.

## Ingress annotation for referring CRDs

An Ingress resource can refer a Rewrite and Responder CRD directly using the `ingress.citrix.com/rewrite-responder` annotation.

The following are different ways of referring the rewrite-responder CRD using annotations.

-  You can apply the Rewrite and Responder CRD for all the services referred in the given ingress using the following format:

        ingress.citrix.com/rewrite-responder_crd: <Rewritepolicy Custom-resoure-instance-name>
  
  Example:

        ingress.citrix.com/rewrite-responder_crd: "blockurlpolicy"
  
  In this example, the Rewrite and Responder policy is applied for all the services referred in the given ingress.

-  You can apply the Rewrite and Responder CRD to a specified Kubernetes service in an Ingress resource using the following format:

        ingress.citrix.com/rewrite-responder_crd: '{<Kubernetes-service-name>: <Rewritepolicy Custom-resoure-instance-name>}'

   Example:

       ingress.citrix.com/rewrite-responder_crd: '{"frontendsvc": "blockurlpolicy", "backendsvc": "addresponseheaders"}'

   In this example, the rewrite policy `blockurlpolicy` is applied on the traffic coming to the `frontendsvc` service and the `addresponseheaders` policy is applied to the `backendsvc` service coming through the current ingress.

You can also apply the Auth, Bot, WAF, and Ratelimit CRDs using ingress annotations:

The following table explains the annotations and examples for Auth, Bot, WAF, and Ratelimit CRDs.

| Annotation                       | Examples                         | Description|
| -------------------              | --------------------------------- |-----------|
| `ingress.citrix.com/bot_crd`       | `ingress.citrix.com/bot_crd: '{"frontend": "botdefense"}'` | Applies the `botdefense` policy to the traffic incoming to the front-end service.|
| `ingress.citrix.com/auth_crd`      | `ingress.citrix.com/auth_crd: '{"frontend": "authexample"}'` | Applies the `authexample` policy to the front-end service. |
| `ingress.citrix.com/waf_crd`       | `ingress.citrix.com/waf_crd: "wafbasic"` | Applies the WAF policy `wafbasic` to all services in the Ingress|
| `ingress.citrix.com/ratelimit_crd` | `ingress.citrix.com/ratelimit_crd: "throttlecoffeeperclientip"` | Applies the rate limit policy `throttlecoffeeperclientip` to all services in the Ingress.|

## Service of type LoadBalancer annotation for referring Rewrite and Responder CRD

A service of type LoadBalancer can refer a Rewrite and Responder CRD using annotations.

The following is the format for the annotation:

    service.citrix.com/rewrite-responder: <Rewritepolicy Custom-resoure-instance-name>
