# Troubleshooting the Citrix ingress controller during runtime

You can debug the Citrix ingress controller using the following methods:

- Event based debugging
- Log based debugging

## Event based debugging

Events are Kubernetes entities which can provide information about the flow of execution on other Kubernetes entities.

Event based debugging for the Citrix ingress controller is enabled at the pod level. To enable event based debugging, the RBAC cluster role permissions for the pod should be same as the cluster role permissions present in the [citrix-k8s-ingress-controller.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/deployment/baremetal/citrix-k8s-ingress-controller.yaml) file.

Use the following command to view the events for the Citrix ingress controller.

        Kubectl describe pods <citrix-k8s-ingress-controller pod name> -n <namespace of pod>

You can view the events under the events section.

In this example, the Citrix ADC has been deliberately made unreachable and the same information can be seen under the events section.

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

            Normal   Created    33m   CIC ENGINE, cic-vpx-functionaltest  CONNECTED: Citrix ADC:<Citrix ADC IP>:80
            Normal   Created    33m   CIC ENGINE, cic-vpx-functionaltest  SUCCESS: Test LB Vserver Creation on Citrix ADC:
            Normal   Created    33m   CIC ENGINE, cic-vpx-functionaltest  SUCCESS: ENABLING INIT features on Citrix ADC:
            Normal   Created    33m   CIC ENGINE, cic-vpx-functionaltest  SUCCESS: GET Default VIP from Citrix ADC:
            Warning  Created    17s   CIC ENGINE, cic-vpx-functionaltest  UNREACHABLE: Citrix ADC: Check Connectivity::<Citrix ADC IP>:80

You can use the events section to check the flow of events within the Citrix ingress controller. Events provide information on the flow of events. For further debugging, you should check logs of the Citrix ingress controller pod.

## Log based debugging

 You can change the log level of the Citrix ingress controller at runtime using the ConfigMap feature. For changing the log level during runtime, see the [ConfigMap](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/configure/config-map/) documentation.

To check logs on the Citrix ingress controller, use the following command.

    kubectl logs <citrix-k8s-ingress-controller> -n namespace
