# Deploy Citrix ingress controller using kops

[Kops](https://github.com/kubernetes/kops) (Kubernetes Operations) is a set of tools for creating and maintaining Kubernetes clusters in the cloud. Using kops, you can also deploy and manage cluster add-ons which extend the functionality of Kubernetes. Citrix provides a [kops add-on](https://github.com/kubernetes/kops/tree/master/addons/ingress-citrix) for deploying Citrix ingress controller.

## Deploy Citrix ingress controller using kops during cluster creation

Perform the following steps to deploy Citrix ingress controller using kops while creating a cluster.

1.  Edit the cluster YAML manifest before creating the cluster.

        kops edit cluster <cluster-name>

1.  Add the Citrix ingress controller add-on specification to the cluster YAML manifest in the section `- spec.addons`.

        addons:
          - manifest: ingress-citrix

For more information on how to enable an add-on during Kubernetes cluster creation, see [kops addon](https://github.com/kubernetes/kops/blob/master/docs/addons.md#installing-kubernetes-addons).

## Deploy Citrix ingress controller using kops after cluster creation

You can use the  `kubectl` command to deploy the Citrix ingress controller add-on with kops after creating the cluster.

        kubectl create secret generic nslogin --from-literal=username='nsroot' --from-literal=password=nsroot
        kubectl create -f https://raw.githubusercontent.com/kubernetes/kops/master/addons/ingress-citrix/v1.1.1.yaml
