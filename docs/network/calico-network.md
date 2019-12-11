# Configure pod to pod communication using Calico

Configuring a network in Kubernetes is a challenge. It requires you to deal with many nodes and pods in a cluster system. There are four problems you need to address while configuring the network:

1.  Container to Container (Which collectively provides a service) communications
1.  Pod to Pod Communication
1.  Pod to Service Communication
1.  External to Service Communication

## Pod to pod communication

By default docker creates a virtual bridge called “docker0” on the host machine and it assigns a private network range to it. For each container that is created, a virtual Ethernet device is attached to this bridge, which is then mapped to eth0 inside the container, with an IP from the network range. This happens for each host that is running docker. There is no coordination between these hosts therefore the network ranges might collide.

Because of this, containers will only able to communicate with containers that are connected to
the same virtual bridge. To communicate with other containers on other hosts, they must rely on port mapping. This means that you need to assign a port on the host machine to each container, and then forward all traffic on that port to that container.

Since local IP address of the application is translated to the host IP address and port on the host machine, Kubernetes assumes that all the nodes can communicate with each other without NAT and that the IP address that a container sees for itself is the same that the other containers see for it. Aside from being simpler, it also enables applications to be ported rather easily from virtual machines to containers, since they do not have to change the way they work in terms of network.

Calico is one of the many different networking options that offer these capabilities for Kubernetes.

## Calico

Calico is designed to simplify, scale, and secure cloud networks. The open source framework
enables Kubernetes networking and network policy for clusters across the cloud. Within the Kubernetes ecosystem, Calico is starting to emerge as one of the most popularly used network frameworks or plug-ins, with many enterprises using it at scale. 

Calico uses a pure IP networking fabric to deliver high performance Kubernetes networking, and its policy engine enforces developer intent for high-level network policy management. Calico provides Layer 3 networking capabilities and associates a virtual router with each node. It enables host to host and pod to pod networking. Calico allows establishment of zone boundaries through BGP or encapsulation through IP on IP or VXLAN methods.

## Integration between Kubernetes and Calico

Calico integrates with Kubernetes through CNI plug-in built on a fully distributed, layer 3 architecture hence it scales smoothly from a single laptop to large enterprise. It relies on an IP layer and it is relatively easy to debug with existing tools.

### Configure the network with Calico

First, bring up a Kubernetes cluster with Calico using the following commands:

    > kubeadm init --pod-network-cidr=192.168.0.0/16
    > export KUBECONFIG=/etc/kubernetes/admin.conf
    > kubectl apply -f calico.yaml

A master node is created with Calico as the CNI. After the master node is up and running, you can join the other nodes to the master using the `join` command.

The Calico process that is part of the Kubernetes master node are:

-  *Calico etcd*

    ```
    kube-system     calico-etcd-j4rwc   1/1     Running
    ```

-  *Calico controller*

    ```
    kube-system     calico-kube-controllers-679568f47c-vz69g        1/1     Running
    ```

-  *Calico nodes*

    ```
    kube-system     calico-node-ct6c9   2/2     Running
    ```

> Note: When you join a node to the Kubernetes cluster, a new *Calico node* is initiated on the Kubernetes node.

### Configure BGP peer with Ingress Citrix ADC

After you have established the Calico network between the master and the other nodes in the cluster, whenever you deploy an application, Kubernetes uses an IP address from the IP address pool of Calico and assigns it to the service associated with the application.

[Border Gateway Protocol (BGP)](https://en.wikipedia.org/wiki/Border_Gateway_Protocol) uses [autonomous system number (AS number)](https://en.wikipedia.org/wiki/Autonomous_system_(Internet)) to identify the remote nodes. The AS number is a special number assigned by IANA used primarily with BGP to identify a network under a single network administration that uses unique routing policy.

#### Configure BGP on Kubernetes using Ingress Citrix ADC

Using a YAML file, you can apply BGP configuration of a remote node using the `kubectl create` command. In the YAML file, you need to add the peer IP address and the AS number. The peer IP address is the Ingress Citrix ADC IP address and the AS number is the AS number that is used in the Ingress Citrix ADC.

#### Obtain the AS Number of the cluster

Using the Calico ctl, you can obtain the AS number used in the Kubernetes cluster by Calico BGP as shown in the following image:

![Get AS number](as-number.png)

#### Configure global BGP peer

Using the `calicoctl` utility you can peer Calico nodes with global BGP speakers. This kind of peers is called global peers.

Create a YAML definition file called `bgp.yml` with the following definition:

```yml
apiVersion: projectcalico.org/v3  # This is the version of Calico
kind: BGPPeer  # BGPPeer specifies that its Global peering.
metadata:
    name: bgppeer-global-3040  # The name of the configuration
spec:
    peerIP: 10.102.33.208  # IP address of the Ingress Citrix ADC
    asNumber: 500  # AS number configured on the Ingress Citrix ADC
```

Deploy the definition file using the following command:

    > kubectl create -f bgp.yml

#### Add the BGP configurations on the Ingress Citrix ADC

Perform the following:

1. Log on to the Citrix ADC command-line interface.
1. Enable the BGP feature using the following command:

        > en feature bgp
          Done

1.  Type `vtysh` and press **Enter**.

        > vtysh
        ns#

1.  Change to config terminal using the `conf t` command:

        ns#conf t
        Enter configuration commands, one per line. End with CNTL/Z.
        ns(config)#

1.  Add the BGP route with the AS number as 500 for demonstration purpose. You can use any number as AS number.

        ns(config)#router bgp 500
        ns(config-router)#

1.  Add neighbors using the following command:

        ns(config-router)#Neighbor 10.102.33.198 remote-as 64512
        ns(config-router)#Neighbor 10.102.22.202 remote-as 64512

1.  Review the running configuration using the following command:

        ns(config-router)#show running-config
        !
        log syslog
        log record-priority
        !
        ns route-install bgp
        !
        interface lo0
         ip adress 127.0.0.1/8
         ipv6 address fe80: :1/64
         ipv6 address : :1/128
        !
        interface vlan0
         ip address 10.102.33.208/24
         ipv6 address fe80::2cf6:beff:fe94:9f63/64
        !
        router bgp 500
         max-paths ebgp 8
         max-paths ibgp 8
         neighbor 10.102.33.198 remote-as 64512
         neighbor 10.102.33.202 remote-as 64512
        !
        end
        ns(config-router)#
    In the sample, the AS number of Calico is 64512, you can change this number as per your requirement.

1.  Install the BGP routes to Citrix ADC routing table using the following command:

        ns(config)#ns route-install bgp
        ns(config)#exit
        ns#exit
         Done
1.  Verify the route add to the routing table using the following command:

    ![Sh route](sh-route.png)

Once the route is installed, the Citrix ADC is able to communicate with the services that are present in the Kubernetes cluster:

![Summary](summary.png)


## Troubleshooting

You can verify BGP configurations on the master node in the Kubernetes cluster using the  `calicoctl` script.

### View the peer IP address and AS number configurations

You can view the peer IP address and AS number configurations using the following command:

    >./calicoctl.1 get bgpPeer
    NAME                    PEERIP          NODE        ASN
    bgppeer-global-3040  10.102.33.208    (global)      500

### View the BGP node status

You can view the status of a BGP node using the following command:

    >calicoctl node status
    IPV4 BGP status
    +---------------+-----------+-------+----------+-------------+
    | PEER ADDRESS | PEER TYPE | STATE | SINCE | INFO |
    +---------------+-----------+-------+----------+-------------+
    | 10.102.33.208 | global | up | 16:38:14 | Established |
    +---------------+-----------+-------+----------+-------------+
