# Support for admission controller webhooks

[Admission controllers](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/) are powerful tools for intercepting requests to the Kubernetes API server prior to the persistence of the object. Using Kubernetes admission controllers, you can define and customize what is allowed to run on your cluster. Hence, they are useful tools for cluster administrators to deploy preventive security controls on your cluster. But you need to compile the admission controllers into the `kube-apiserver` binary and they offer limited flexibility.

To overcome this limitation, Kubernetes supports dynamic admission controllers that can be developed as extensions and run as webhooks configured at runtime.
Using the [Admission controller webhooks](https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/#admission-webhooks) Kubernetes cluster administrators can create additional plug-ins to the admission chain of API server without recompiling them. Admission controller webhooks can be executed whenever a resource is created, updated, or deleted.

You can define two types of admission controller webhooks:

- validating admission webhook
- mutating admission webhook

 Mutating admission webhooks are invoked first, and they can modify objects sent to the API server to enforce custom defaults. Once all the object modifications are complete, and the incoming object is validated by the API server, validating admission webhooks are invoked. Validating admission hooks process requests and accept or reject requests to enforce custom
  policies.

The following diagram explains how the admission controller webhook works:

![admission-control-webhook](.././media/admission-controller-webhook.png)

Here are some of the scenarios where admission webhooks are useful:

- To mandate a reasonable security baseline across an entire namespace or cluster mandating. For example, disallowing containers from running as root or making sure the container’s root filesystem is always mounted as read-only.
- To enforce the adherence to certain standard and practices for labels, annotations, or resource limits. For example, enforce label validation on different objects to ensure proper labels are being used for various objects.
  
- To validate the configuration of the objects running in the cluster and prevent any obvious misconfigurations from hitting your cluster.
For example, to detect and fix images deployed without semantic tags.

For more information, see [Support for admission controller webhooks](https://docs.citrix.com/en-us/citrix-k8s-ingress-controller/how-to/webhook-use-case.html).