# Configuring consistent hashing algorithm using Citrix ingress controller

Load balancing algorithms define the criteria that the Citrix ADC appliance uses to select the service to which to redirect each client request. Different load balancing algorithms use different criteria and consistent hashing is one the load balancing algorithms supported by Citrix ADC.
Consistent hashing algorithms are often used to load balance when the back-end is a caching server to achieve stateless persistency.
Consistent hashing can ensure that when a cache server is removed, only the requests cached in that specific server is rehashed and the rest of the requests are not affected. For more information on the consistent hashing algorithm, see the [Citrix ADC documentation](https://docs.citrix.com/en-us/citrix-adc/current-release/load-balancing/load-balancing-customizing-algorithms/hashing-methods.html#consistent-hashing-algorithms).

You can now configure the consistent hashing algorithm on Citrix ADC using Citrix ingress controller. This configuration is enabled with in the Citrix ingress controller using a ConfigMap.

## Configure hashing algorithm

A new parameter `NS_LB_HASH_ALGO` is introduced in the Citrix ingress controller ConfigMap for hashing algorithm support.
Supported environment variables for consistent hashing algorithm using ConfigMap under the `NS_LB_HASH_ALGO` parameter:

-  `hashFingers`: Specifies the number of fingers to be used for the hashing algorithm. Possible values are from 1 to 1024. Increasing the number of fingers provides better distribution of traffic at the expense of extra memory.
-  `hashAlgorithm`: Specifies the supported algorithm. Supported algorithms are `default`, `jarh`, `prac`.

The following example shows a sample ConfigMap for configuring consistent hashing algorithm using Citrix ingress controller. In this example, the hashing algorithm is used as Prime Re-Shuffled Assisted CARP (PRAC) and the number of fingers to be used in PRAC is set as 50.

        apiVersion: v1
        kind: ConfigMap
        metadata:
        name: cic-configmap
        labels:
            app: citrix-ingress-controller
        data:
        NS_LB_HASH_ALGO: |
            hashFingers: 50
            hashAlgorithm: 'prac'
