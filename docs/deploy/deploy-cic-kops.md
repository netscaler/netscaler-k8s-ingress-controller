# Deploy Citrix ingress controller using kops

[Kops](https://github.com/kubernetes/kops) (Kubernetes Operations) is a set of tools for creating and maintaining Kubernetes clusters in the cloud. Using kops, you can also deploy and manage cluster add-ons which extend the functionality of Kubernetes. Citrix provides a [kops add-on](https://github.com/kubernetes/kops/tree/master/addons/ingress-citrix) for deploying Citrix ingress controller.

## Deploy Citrix ingress controller using kops during cluster creation

Perform the following steps to deploy Citrix ingress controller using kops while creating a cluster on Google Cloud Platform (GCP) from a YAML manifest.

1.  Edit the cluster YAML manifest before creating the cluster.

1.  Add the Citrix ingress controller add-on specification to the cluster YAML manifest in the section `- spec.addons`.

    !!! note "Note"
        The steps in this procedure are applicable only for GCP. For deploying the Citrix ingress controller add-on using kops on AWS, see [Deploy Citrix ingress controller using kops after cluster creation](#deploy-citrix-ingress-controller-using-kops-during-cluster-creation).

For more information on how to enable an add-on during Kubernetes cluster creation, see [kops addon](https://github.com/kubernetes/kops/blob/master/docs/addons.md#installing-kubernetes-addons).

## Deploy Citrix ingress controller using kops after cluster creation

You can use the  `kubectl` command to deploy the Citrix ingress controller add-on with kops after creating the cluster.

-  **For GCP:**  Use the following command to deploy Citrix ingress controller in GCP after the cluster creation:

        kubectl create -f https://raw.githubusercontent.com/kubernetes/kops/master/addons/ingress-citrix/v1.1.1.yaml

-  **For AWS:** Use the following command to deploy Citrix ingress controller in AWS after the cluster creation:

        kubectl create -f https://raw.githubusercontent.com/kubernetes/kops/master/addons/ingress-citrix/v1.1.1-aws.yaml
