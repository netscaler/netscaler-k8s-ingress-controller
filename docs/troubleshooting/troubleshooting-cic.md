# Troubleshooting the Citrix ingress controller during runtime

You can use te following tools available with Citrix ingress controller to help you in troubleshooting.

## Kubectl plug-in for NetScaler

NetScaler provides a [kubectl plug-in](https://github.com/netscaler/modern-apps-toolkit/tree/main/netscaler-plugin) to inspect ingress controller deployments and aids in troubleshooting operations. You can inspect the NetScaler configuration and related Kubernetes components using the subcommands available with this plug-in.

Using the [support subcommand](https://github.com/netscaler/modern-apps-toolkit/tree/main/netscaler-plugin#support-command) you can get NetScaler (show techsupport) and ingress controller support bundle.

You can collect and share the support bundle information with the support team for faster resolution.

## Citrix ingress controller diagnostics Tool

[Citrix ingress controller diagnostics tool](https://github.com/netscaler/modern-apps-toolkit/tree/main/cic_diagnostics_tool) is a simple shell script that collects information related to Citrix ingress Controller and applications deployed in the Kubernetes cluster.

## Helpful commands for troubleshooting

You can debug the Citrix ingress controller using the following methods:

-  Event based debugging
-  Log based debugging

Providing the outputs of the commands in this section helps the support team in troubleshooting Citrix ingress controller.

### Event based debugging

Events are Kubernetes entities which can provide information about the flow of execution on other Kubernetes entities.

Event based debugging for the Citrix ingress controller is enabled at the pod level. To enable event-based debugging, the RBAC cluster role permissions for the pod should be same as the cluster role permissions present in the [citrix-k8s-ingress-controller.yaml](https://github.com/netscaler/netscaler-k8s-ingress-controller/blob/master/deployment/baremetal/citrix-k8s-ingress-controller.yaml) file.

Use the following command to view the events for the Citrix ingress controller.

        Kubectl describe pods <citrix-k8s-ingress-controller pod name> -n <namespace of pod>

You can view the events under the events section.

In this example, the Netscaler has been deliberately made unreachable and the same information can be seen under the events section.

            kubectl describe pods cic-vpx-functionaltest -n functionaltest

            Name:         cic-vpx-functionaltest
            Namespace:    functionaltest

            Events:
            Type     Reason     Age   From                                Message
            ----     ------     ----  ----                                -------
            Normal   Pulled     33m   kubelet, rak-asp4-node2             Container image "citrix-ingress-controller:latest" already present on machine
            Normal   Created    33m   kubelet, rak-asp4-node2             Created container cic-vpx-functionaltest
            Normal   Started    33m   kubelet, rak-asp4-node2             Started container cic-vpx-functionaltest
            Normal   Scheduled  33m   default-scheduler                   Successfully assigned functionaltest/cic-vpx-functionaltest to rak-asp4-node2

            Normal   Created    33m   CIC ENGINE, cic-vpx-functionaltest  CONNECTED: Netscaler:<Netscaler IP>:80
            Normal   Created    33m   CIC ENGINE, cic-vpx-functionaltest  SUCCESS: Test LB Vserver Creation on Netscaler:
            Normal   Created    33m   CIC ENGINE, cic-vpx-functionaltest  SUCCESS: ENABLING INIT features on Netscaler:
            Normal   Created    33m   CIC ENGINE, cic-vpx-functionaltest  SUCCESS: GET Default VIP from Netscaler:
            Warning  Created    17s   CIC ENGINE, cic-vpx-functionaltest  UNREACHABLE: Netscaler: Check Connectivity::<Netscaler IP>:80

You can use the events section to check the flow of events within the Citrix ingress controller. Events provide information on the flow of events. For further debugging, you should check the logs of the Citrix ingress controller pod.

### Log based debugging

 You can change the log level of the Citrix ingress controller at runtime using the ConfigMap feature. For changing the log level during runtime, see the [ConfigMap](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/configure/config-map/) documentation.

To check logs on the Citrix ingress controller, use the following command.

    kubectl logs <citrix-k8s-ingress-controller> -n namespace
