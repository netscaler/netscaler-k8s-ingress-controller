# **Custom Resource Definitions**

A custom resource definition (CRD) file defines our own object kinds and lets the Kubernetes API Server handle the entire lifecycle. For more information please see [Kubernetes Custom Resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/).

The above YAML is the deployment file of CRD supported by Netscaler ingress controller. Detailed information on how to use the CRD, see [Use Rewrite and Responder policies in Kubernetes](../docs/crds/rewrite-responder.md).

## CRDs for NetScaler Kubernetes Gateway Controller

These CRDs are used with NetScaler Kubernetes Gateway Controller:

-  [mcp/mcpprofile.yaml](mcp/mcpprofile.yaml) and [mcp/mcproute.yaml](mcp/mcproute.yaml): MCPProfile and MCPRoute, for NetScaler as an MCP (Model Context Protocol) gateway. For more information, see [MCPProfile](https://docs.netscaler.com/us/en/netscaler-kubernetes-gateway-controller/crds/mcpprofile.html) and [MCPRoute](https://docs.netscaler.com/us/en/netscaler-kubernetes-gateway-controller/crds/mcproute.html).
-  [aigateway/aigatewayprofile.yaml](aigateway/aigatewayprofile.yaml) and [aigateway/aigatewayroute.yaml](aigateway/aigatewayroute.yaml): AIGatewayProfile and AIGatewayRoute, for NetScaler as an AI gateway. For more information, see [AIGatewayProfile](https://docs.netscaler.com/us/en/netscaler-kubernetes-gateway-controller/crds/aigatewayprofile.html) and [AIGatewayRoute](https://docs.netscaler.com/us/en/netscaler-kubernetes-gateway-controller/crds/aigatewayroute.html).
