# Citrix API Gateway for Kubernetes

An API gateway acts as the single entry point for your APIs and ensures secure and reliable access to multiple APIs and microservices in your system.

Citrix provides an enterprise grade API gateway for North-South API traffic into the Kubernetes cluster. The API gateway integrates with Kubernetes through the Citrix ingress controller and the Citrix ADC (Citrix ADC MPX, VPX, or CPX) deployed as the Ingress Gateway for on-premises or cloud deployments.

The following diagram shows a dual-tier topology for the API gateway.

![API Gateway](../media/citrix-api-gateway.png)

Using the API gateway offered by Citrix, you can perform the following functionalities:

- Enforce authentication policies
- Rate limit access to services
- Advanced content routing
- Flexible and comprehensive transformation of HTTP transactions using the rewrite and responder policies
- Enforce web application firewall policies

## How does the API gateway work

 Citrix API gateway is built on top of the Citrix ingress gateway and leverages Kubernetes API extensions such as custom resource definitions (CRDs). Using CRDs, you can automatically configure a Citrix ADC and API gateway in the same instance.

Citrix provides the following CRDs for the API gateway:

- [Auth CRD](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/crd/auth/auth-crd.yaml)
- [Rate limit CRD](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/crd/ratelimit/README.md)
- [Content routing CRD](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/crd/contentrouting/README.md)
- [Rewrite and responder CRD](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/crd/rewrite-responder-policies-deployment.yaml)
- [WAF CRD](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/crd/waf/waf-crd.yaml)

## Key benefits of using the API gateway

Following are the key benefits of the API gateway offered by Citrix:

- Leverages the advanced traffic management and comprehensive security features of Citrix ADC
- Optimizes your deployments by consolidating multiple network functions into a single component of the Citrix Ingress Gateway.
- Reduces the operational complexity and cost involved in deploying multiple components
- Ensures better performance for your application traffic by reducing multiple hops of TCP or TLS decryption while using separate components
- Simplifies deploy and integrate in your Kubernetes environments either by directly using YAMLs or helm charts

## Deploying Citrix API gateway

For more information on how to configure Citrix API gateway features using CRDs, see the following:

- [Authentication](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/crds/auth/)
- [Rate limiting](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/crds/rate-limit/)
- [Advanced content routing](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/crds/content-routing/)
- [Rewrite and responder policies](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/crds/rewrite-responder/)
- [Web application firewall policies](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/crds/waf/)
