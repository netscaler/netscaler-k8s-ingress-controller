# Admission controller

Please refer kubernetes documentation for using [admission controllers](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/).

An admission controller is a piece of code that intercepts requests to the Kubernetes API server prior to persistence of the object, but after the request is authenticated and authorized. The controllers are compiled into the kube-apiserver binary, and may only be configured by the cluster administrator. 

The admission control process has two phases: the mutating phase is executed first, followed by the validating phase. (image [credit](https://kubernetes.io/blog/2019/03/21/a-guide-to-kubernetes-admission-controllers/))
![admission-controller-phases](../media/admission-controller-phases.png)
Among the more than 30 admission controllers shipped with Kubernetes, two take a special role because of their nearly limitless flexibility -

MutatingAdmissionWebhook: can modify objects by creating a patch that will be sent back in the admission response.

ValidatingAdmissionWebhook. Matching webhooks are called in parallel; validating webhooks can reject a request, but they cannot modify the object they are receiving in the admission request.

*If any of webhook rejects a request, an error is returned to the end-user and resource will not be applied. Kubernetes recommends the following admission controllers to be enabled by default.



# Why do I need admission controllers?
If your organization has been operating Kubernetes, you probably have been looking for ways to control what end-users can do on the cluster and ways to ensure that clusters are in compliance with company policies.

## Security: 
Admission controllers can increase security by mandating a reasonable security baseline across an entire namespace or cluster. e.g.
* Allow pulling images only from specific registries known to the enterprise, while denying unknown image registries.
* Secure ingress by making TLS as mandatory and validate for secure annotation
* Deny a pod from running on the cluster if it matches certain restricted label

## Governance:
Admission controllers allow you to enforce the adherence to certain practices such as having good labels, annotations, resource limits, or other settings. e.g.
* Enforce label validation on different objects to ensure proper labels are being used for various objects, such as every object being assigned to a team or project, or every deployment specifying an app label.
* Automatically add annotations to objects, such as attributing the correct cost center for a “dev” deployment resource.

## Configuration management: 
Admission controllers allow you to validate the configuration of the objects running in the cluster and prevent any obvious misconfigurations from hitting your cluster. Admission controllers can be useful in detecting and fixing images deployed without semantic tags, such as by:
* automatically adding resource limits or validating resource limits,
* ensuring reasonable labels are added to pods, or
* ensuring image references used in production deployments are not using the latest tags, or tags with a -dev suffix.
* Two ingresses in different namespaces must not have the same hostname.

# How do I apply admission controllers?

## [OPA](https://github.com/open-policy-agent) (Open Policy Agent)
Open source, general-purpose policy engine that unifies policy enforcement across the stack. OPA provides a high-level declarative language (Rego) that let’s you specify policy as code and simple APIs to offload policy decision-making from your software. You can use OPA to enforce policies in microservices, Kubernetes, CI/CD pipelines, API gateways, and more.  It has become a standard practice for writing admission controls.

## [Gatekeeper](https://github.com/open-policy-agent/gatekeeper)
Gatekeeper is a customizable validating (mutating TBA) webhook that enforces CRD-based policies executed by OPA.
![gatekeeper](../media/gatekeeper.png)(image [credit](https://kubernetes.io/blog/2019/08/06/opa-gatekeeper-policy-and-governance-for-kubernetes/))
### How is Gatekeeper different from OPA?
 Compared to using OPA with its sidecar kube-mgmt (aka Gatekeeper v1.0), Gatekeeper introduces the following functionality:
* An extensible, parameterized policy library
Native Kubernetes CRDs for instantiating the policy library (aka "constraints")
* Native Kubernetes CRDs for extending the policy library (aka "constraint templates")
* Audit functionality

# Writing and Deploying an Admission Controller Webhook
## Prerequisites

Kubernetes 1.14.0 or above with the admissionregistration.k8s.io/v1beta1 API enabled. Verify that by the following command:

    kubectl api-versions | grep admissionregistration.k8s.io/v1beta1
    The result should be:
    admissionregistration.k8s.io/v1beta1

In addition, the MutatingAdmissionWebhook and ValidatingAdmissionWebhook admission controllers should be added and listed in the correct order in the admission-control flag of kube-apiserver. With Minikube, this is done by starting minkube with
        
        minikube start --extra-config=apiserver.enable-admission-plugins=NamespaceLifecycle,LimitRanger,ServiceAccount,DefaultStorageClass,DefaultTolerationSeconds,NodeRestriction,MutatingAdmissionWebhook,ValidatingAdmissionWebhook`

RBAC Permissions
For either installation method, make sure you have cluster admin permissions:

    kubectl create clusterrolebinding cluster-admin-binding --clusterrole cluster-admin --user <YOUR USER NAME>

## Mutating Admission Webhook Configuration
Please refer [ingress-admission-webhook](https://github.com/citrix/ingress-admission-webhook) for details.

Use cases covered
* Update port in ingress based on ingress name 
* Enable secure backend forcefully based on namespace
  
## Validating Admission Webhook Configuration using Gatekeeper
Gatekeeper uses CRD that allows users to create constraints as kubernetes resources. That’s called a “ConstraintTemplate” in Gatekeeper.  The schema of the constraint allows an admin to fine-tune the behavior of a constraint, much like arguments to a function. Constraints used to inform Gatekeeper that the admin wants a ConstraintTemplate to be enforced, and how.

We can apply various polices using ConstraintTemplates, various examples are listed at [Gatekeeper library](https://github.com/open-policy-agent/gatekeeper/tree/master/library).

Lets take one example of one policy of validating httpsonly policy  to understand how it works:

### Quick Start - HttpsOnly Policy

1. Install Gatekeeper

    You can install gatekeeper using various methods mentioned at Gatekeeper installation.  Here, we are using prebuilt image:

    Deploying a Release using Prebuilt Image

        > kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper/master/deploy/gatekeeper.yaml

        namespace/gatekeeper-system created

        customresourcedefinition.apiextensions.k8s.io/configs.config.gatekeeper.sh created

        serviceaccount/gatekeeper-admin created

        role.rbac.authorization.k8s.io/gatekeeper-manager-role created

        clusterrole.rbac.authorization.k8s.io/gatekeeper-manager-role created

        rolebinding.rbac.authorization.k8s.io/gatekeeper-manager-rolebinding created

        clusterrolebinding.rbac.authorization.k8s.io/gatekeeper-manager-rolebinding created

        secret/gatekeeper-webhook-server-cert created

        service/gatekeeper-webhook-service created

        deployment.apps/gatekeeper-controller-manager created

        validatingwebhookconfiguration.admissionregistration.k8s.io/gatekeeper-validating-webhook-configuration created

        customresourcedefinition.apiextensions.k8s.io/constrainttemplates.templates.gatekeeper.sh created
   Verify installation
   > kubectl get crd | grep -i constraint
    constrainttemplates.templates.gatekeeper.sh   2020-04-18T14:10:49Z
    
*You can check all ConstraintTemplate using below command: 
    kubectl get constrainttemplates.templates.gatekeeper.sh
    
2. Apply httpsonly ConstraintTemplate
    kubectl apply -f webhook/httpsonly/template.yaml
3. Apply constraint to enforce httpsonly policy
   kubectl apply -f webhook/httpsonly/constraint.yaml
4. Verify with sample ingress which violates policy
   kubectl apply -f webhook/httpsonly/bad-example-ingress.yaml
   
   This will throw error 
   Error from server ([denied by ingress-https-only] Ingress must be https. tls configuration is required for test-ingress): error when creating "ingress.yaml": admission webhook "validation.gatekeeper.sh" denied the request: [denied by ingress-https-only] Ingress must be https. tls configuration is required for test-ingress

5. Now, apply ingress which has required TLS section in ingress
   kubectl apply -f  webhook/httpsonly/good-example-ingress.yaml
   It will be applied succesfully.
   ingress.networking.k8s.io/test-ingress created
6. Clean up once done all verfication of gatekeeper policies.
   Uninstall all packages and template installed.
   kubectl delete -f webhook/httpsonly/good-example-ingress.yaml
   kubectl delete -f webhook/httpsonly/constraint.yaml
   kubectl delete -f webhook/httpsonly/template.yaml
   kubectl delete -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper/master/deploy/gatekeeper.yaml

# Sample Use Cases
There are multiple use cases listed under webhook directory. Steps will be similar what we have done above:
1. Apply template yaml given in each usecase dir
2. Apply Constraint yaml 
3. Verify bad/good sample yamls to validate use case.