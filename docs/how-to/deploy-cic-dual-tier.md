# How to set up dual-tier deployment

In a dual-tier deployment, Citrix ADC VPX or MPX is deployed outside the Kubernetes cluster (Tier-1) and Citrix ADC CPXs are deployed inside the Kubernetes cluster (Tier-2).

Citrix ADC MPX or VPX devices in Tier-1 proxy the traffic (North-South) from the client to Citrix ADC CPXs in Tier-2. The Tier-2 Citrix ADC CPX then routes the traffic to the microservices in the Kubernetes cluster. The Citrix ingress controller deployed as a standalone pod configures the Tier-1 Citrix ADC. And, the sidecar Citrix ingress controller in one or more Citrix ADC CPX pods configures the associated Citrix ADC CPX in the same pod.

The Dual-Tier deployment can be set up on Kubernetes in bare metal environment or on public clouds such as, AWS, GCP, or Azure.

The following diagram shows a Dual-Tier deployment:
![Dual-Tier deployment](../media/dualtier.png)

## Setup process

The Citrix ingress controller [repo](https://github.com/citrix/citrix-k8s-ingress-controller) provides a sample Apache microservice and manifests for Citrix ADC CPX for Tier-2, ingress object for Tier-2 Citrix ADC CPX, Citrix ingress controller, and an ingress object for Tier-1 Citrix ADC for demonstration purpose. These samples are used in the setup process to deploy a dual-tier topology.

Perform the following:

1.  Create a Kubernetes cluster in cloud or on-premises. The Kubernetes cluster in cloud can be a managed Kubernetes (for example: GKE, EKS, or AKS) or a custom created Kubernetes deployment.

1.  Deploy Citrix ADC MPX or VPX on a multi-NIC deployment mode outside the Kubernetes cluster.
    -  For instructions to deploy Citrix ADC MPX, see [Citrix ADC documentation](https://docs.citrix.com/en-us/citrix-adc/13).

    -  For instructions to deploy Citrix ADC VPX, see [Deploy a Citrix ADC VPX instance](https://docs.citrix.com/en-us/citrix-adc/13/deploying-vpx.html).

    Perform the following after you deploy Citrix ADC VPX or MPX:

    1.  Configure an IP address from the subnet of the Kubernetes cluster as SNIP on the Citrix ADC. For information on configuring SNIPs in Citrix ADC, see [Configuring Subnet IP Addresses (SNIPs)](https://docs.citrix.com/en-us/citrix-adc/13/networking/ip-addressing/configuring-citrix-adc-owned-ip-addresses/configuring-subnet-ip-addresses-snips.html).

    1.  Enable management access for the SNIP that is the same subnet of the Kubernetes cluster. The SNIP should be used as `NS_IP` variable in the [Citrix ingress controller YAML](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/dual-tier/manifest/tier-1-vpx-cic.yaml) file to enable Citrix ingress controller to configure the Tier-1 Citrix ADC.

        !!! note "Note"
            It is not mandatory to use SNIP as `NS_IP`. If the management IP address of the Citrix ADC is reachable from Citrix ingress controller then you can use the management IP address as `NS_IP`.

    1.  In cloud deployments, enable [MAC-Based Forwarding mode](https://docs.citrix.com/en-us/citrix-adc/13/networking/interfaces/configuring-mac-based-forwarding.html) on the Tier-1 Citrix ADC VPX. As Citrix ADC VPX is deployed in multi-NIC mode, it would not have the return route to reach the POD CNI network or the Client network. Hence, you need to enable MAC-Based Forwarding mode on the Tier-1 Citrix ADC VPX to handle this scenario.

    1.  Create a [Citrix ADC system user account](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/deploy/deploy-cic-yaml/#create-system-user-account-for-citrix-ingress-controller-in-citrix-adc) specific to Citrix ingress controller. Citrix ingress controller uses the system user account to automatically configure the Tier-1 Citrix ADC.

    1.  Configure your on-premises firewall or security groups on your cloud to allow inbound traffic to the ports required for Citrix ADC. The Setup process uses port 80 and port 443, you can modify these ports based on your requirement.

1.  Deploy a sample microservice. Use the following command:

        kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/dual-tier/manifest/apache.yaml

1.  Deploy Citrix ADC CPX as Tier-2 ingress. Use the following command:

        kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/dual-tier/manifest/tier-2-cpx.yaml

1.  Create an ingress object for the Tier-2 Citrix ADC CPX. Use the following command:

        kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/dual-tier/manifest/ingress-tier-2-cpx.yaml

1.  Deploy the Citrix ingress controller for Tier-1 Citrix ADC. Perform the following:

    1.  Download the Citrix ingress controller manifest file. Use the following command:

            wget https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/dual-tier/manifest/tier-1-vpx-cic.yaml

    1.  Edit the Citrix ingress controller manifest file and enter the values for the following environmental variables:

        | Environment Variable | Mandatory or Optional | Description |
        | ---------------------- | ---------------------- | ----------- |
        | NS_IP | Mandatory | The IP address of the Citrix ADC appliance. For more details, see [Prerequisites](../deploy/deploy-cic-yaml.md#prerequisites). |
        | NS_USER and NS_PASSWORD | Mandatory | The user name and password of the Citrix ADC VPX or MPX appliance used as the Ingress device. For more details, see [Prerequisites](../deploy/deploy-cic-yaml.md#prerequisites). |
        | EULA | Mandatory | The End User License Agreement. Specify the value as `Yes`.|
        | LOGLEVEL | Optional | The log levels to control the logs generated by Citrix ingress controller. By default, the value is set to DEBUG. The supported values are: CRITICAL, ERROR, WARNING, INFO, and DEBUG. For more information, see [Log Levels](../configure/log-levels.md)|
        | NS_PROTOCOL and NS_PORT | Optional | Defines the protocol and port that must be used by Citrix ingress controller to communicate with Citrix ADC. By default, Citrix ingress controller uses HTTPS on port 443. You can also use HTTP on port 80. |
        | ingress-classes | Optional | If multiple ingress load balancers are used to load balance different ingress resources. You can use this environment variable to specify Citrix ingress controller to configure Citrix ADC associated with specific ingress class. For information on Ingress classes, see [Ingress class support](../configure/ingress-classes.md)|
        | NS_VIP | Optional | Citrix ingress controller uses the IP address provided in this environment variable to configure a virtual IP address to the Citrix ADC that receives Ingress traffic. **Note:** NS_VIP takes precedence over the [frontend-ip](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/annotations.md) annotation. |

    1.  Deploy the updated Citrix ingress controller manifest file. Use the following command:

            kubectl create -f tier-1-vpx-cic.yaml

1.  Create an ingress object for the Tier-1 Citrix ADC. Use the following command:

        kubectl create -f https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/dual-tier/manifest/ingress-tier-1-vpx.yaml

1.  Update DNS server details in the cloud or on-premises to point your website to the VIP of the Tier-1 Citrix ADC.

    For example: `citrix-ingress.com 192.250.9.1`

    Where `192.250.9.1` is the VIP of the Tier-1 Citrix ADC and `citrix-ingress.com` is the microservice running in your Kubernetes cluster.

1.  Access the URL of the microservice to verify the deployment.

## Set up dual-tier deployment using one step deployment manifest file

For easy deployment, the Citrix ingress controller [repo](https://github.com/citrix/citrix-k8s-ingress-controller) includes an all-in-one deployment manifest. You can download the file and update it with values for the following environmental variables and deploy the manifest file.

!!! note "Note"
    Ensure that you have completed step 1–2 in the [Setup process](#setup-process).

Perform the following:

1.  Download the all-in-one deployment manifest file. Use the following command:

        wget https://raw.githubusercontent.com/citrix/citrix-k8s-ingress-controller/master/deployment/dual-tier/manifest/all-in-one-dual-tier-demo.yaml

1.  Edit the all-in-one deployment manifest file and enter the values for the following environmental variables:

    | Environment Variable | Mandatory or Optional | Description |
    | ---------------------- | ---------------------- | ----------- |
    | NS_IP | Mandatory | The IP address of the Citrix ADC appliance. For more details, see [Prerequisites](../deploy/deploy-cic-yaml.md#prerequisites). |
    | NS_USER and NS_PASSWORD | Mandatory | The user name and password of the Citrix ADC VPX or MPX appliance used as the Ingress device. For more details, see [Prerequisites](../deploy/deploy-cic-yaml.md#prerequisites). |
    | EULA | Mandatory | The End User License Agreement. Specify the value as `Yes`.|
    | LOGLEVEL | Optional | The log levels to control the logs generated by Citrix ingress controller. By default, the value is set to DEBUG. The supported values are: CRITICAL, ERROR, WARNING, INFO, and DEBUG. For more information, see [Log Levels](../configure/log-levels.md)|
    | NS_PROTOCOL and NS_PORT | Optional | Defines the protocol and port that must be used by Citrix ingress controller to communicate with Citrix ADC. By default, Citrix ingress controller uses HTTPS on port 443. You can also use HTTP on port 80. |
    | ingress-classes | Optional | If multiple ingress load balancers are used to load balance different ingress resources. You can use this environment variable to specify Citrix ingress controller to configure Citrix ADC associated with specific ingress class. For information on Ingress classes, see [Ingress class support](../configure/ingress-classes.md)|
    | NS_VIP | Optional | Citrix ingress controller uses the IP address provided in this environment variable to configure a virtual IP address to the Citrix ADC that receives Ingress traffic. **Note:** NS_VIP acts as a fallback when the [frontend-ip](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/configure/annotations.md) annotation is not provided in Ingress yaml. Not supported for Type Loadbalancer service. |

1.  Deploy the updated all-in-one deployment manifest file. Use the following command:

        kubectl create -f all-in-one-dual-tier-demo.yaml
