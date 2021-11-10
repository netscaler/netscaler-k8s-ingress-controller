# Deploying a Citrix ADC CPX Instance in Docker
This guide provides the step-by-step approach to deploy a Citrix ADC CPX on docker in Linux environment.

## Pre-requisites:
[Linux machine with docker] (https://docs.docker.com/v17.12/install/#supported-platforms)

## System Requirements:
   * RAM : 2 GB
   * CPU : 1

## Pulling Citrix ADC CPX docker image:
Use the following command to pull the CPX image from quay

```
docker pull quay.io/citrix/citrix-k8s-cpx-ingress:13.0-83.27 
```

Use the following command to verify if CPX image is installed in docker images

```
root@ubuntu:~# docker images | grep 'citrix-k8s-cpx-ingress'
quay.io/citrix/citrix-k8s-cpx-ingress                  13.0-83.27          952a04e73101        2 months ago        469 MB
```

## Using 'docker run' command to deploy CPX container:
Use the following command to create a CPX container instance running in bridge mode

```
docker run -dt -P --privileged=true -e EULA=yes --ulimit core=-1 --name cpx-hello-world quay.io/citrix/citrix-k8s-cpx-ingress:13.0-83.27 
```

Use the following command to verify if the CPX container is created successfully

```
root@ubuntu:~# docker ps | grep cpx-hello-world
00d58f020a9e        quay.io/citrix/citrix-k8s-cpx-ingress:13.0-83.27   "/var/netscaler/bi..."   5 seconds ago       Up 3 seconds        0.0.0.0:33122->22/tcp, 0.0.0.0:32770->161/udp, 0.0.0.0:33121->9080/tcp, 0.0.0.0:33120->9443/tcp   cpx-hello-world
```

If the above verification fails, please check container logs for the error logs

```
docker logs cpx-hello-world
```

Once CPX container is deployed successfully, the following command can be used to access the Shell of CPX container

```
docker exec -it cpx-hello-world bash
```

Use Ctrl+D or 'exit' command to return to Linux host's Shell

CPX container can also be accessed using SSH. For that we need the IP of CPX container which can be fetched using the following command and the default username is 'nsroot' and default password is 'nsroot'

```
root@ubuntu:~# docker exec cpx-hello-world cli_script.sh "show ns ip"
exec: show ns ip
        Ipaddress        Traffic Domain  Type             Mode     Arp      Icmp     Vserver  State
        ---------        --------------  ----             ----     ---      ----     -------  ------
1)      172.17.0.6       0               NetScaler IP     Active   Enabled  Enabled  NA       Enabled
2)      192.0.0.1        0               SNIP             Active   Enabled  Enabled  NA       Enabled
Done

root@ubuntu:~# ssh nsroot@172.17.0.6
The authenticity of host '172.17.0.6 (172.17.0.6)' can't be established.
ECDSA key fingerprint is SHA256:Pfrv9PCkAnmQG8B+dii1GPQC1+GV/xuZbT/D7QJ8ac8.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '172.17.0.6' (ECDSA) to the list of known hosts.
nsroot@172.17.0.6's password:
Welcome to nsoslx 1.0 (GNU/Linux 4.4.0-116-generic x86_64)

 * Documentation:  https://www.citrix.com/

The programs included with the nsoslx system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

nsoslx comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

root@00d58f020a9e:~# cli_script.sh "show ns ip"
exec: show ns ip
        Ipaddress        Traffic Domain  Type             Mode     Arp      Icmp     Vserver  State
        ---------        --------------  ----             ----     ---      ----     -------  ------
1)      172.17.0.6       0               NetScaler IP     Active   Enabled  Enabled  NA       Enabled
2)      192.0.0.1        0               SNIP             Active   Enabled  Enabled  NA       Enabled
Done
root@00d58f020a9e:~#
```


## Using CLI/NITRO on Citrix ADC CPX
CPX can be configured using **cli_script.sh** or **NITRO API** calls

Using **cli_script.sh** (Requires execution from CPX Shell)

```
root@00d58f020a9e:~# cli_script.sh "show ns ip"
exec: show ns ip
        Ipaddress        Traffic Domain  Type             Mode     Arp      Icmp     Vserver  State
        ---------        --------------  ----             ----     ---      ----     -------  ------
1)      172.17.0.6       0               NetScaler IP     Active   Enabled  Enabled  NA       Enabled
2)      192.0.0.1        0               SNIP             Active   Enabled  Enabled  NA       Enabled
Done
```

Using **NITRO API** (Requires execution from Linux host's Shell)

```
root@ubuntu:~# curl -u nsroot:nsroot http://172.17.0.6:9080/nitro/v1/config/nsip
{ "errorcode": 0, "message": "Done", "severity": "NONE", "nsip": [ { "ipaddress": "172.17.0.6", "td": "0", "type": "NSIP", "netmask": "255.255.0.0", "flags": "40", "arp": "ENABLED", "icmp": "ENABLED", "vserver": "ENABLED", "telnet": "ENABLED", "ssh": "ENABLED", "gui": "ENABLED", "snmp": "ENABLED", "ftp": "ENABLED", "mgmtaccess": "ENABLED", "restrictaccess": "DISABLED", "decrementttl": "DISABLED", "dynamicrouting": "ENABLED", "hostroute": "DISABLED", "advertiseondefaultpartition": "DISABLED", "networkroute": "DISABLED", "tag": "0", "hostrtgwact": "0.0.0.0", "metric": 0, "ospfareaval": "0", "vserverrhilevel": "ONE_VSERVER", "vserverrhimode": "DYNAMIC_ROUTING", "viprtadv2bsd": false, "vipvsercount": "0", "vipvserdowncount": "1", "vipvsrvrrhiactivecount": "0", "vipvsrvrrhiactiveupcount": "0", "ospflsatype": "TYPE5", "state": "ENABLED", "freeports": "1032095", "riserhimsgcode": 32, "iptype": [ "NSIP" ], "icmpresponse": "NONE", "ownernode": "255", "arpresponse": "NONE", "ownerdownresponse": "YES" }, { "ipaddress": "192.0.0.1", "td": "0", "type": "SNIP", "netmask": "255.255.255.0", "flags": "8", "arp": "ENABLED", "icmp": "ENABLED", "vserver": "DISABLED", "telnet": "DISABLED", "ssh": "DISABLED", "gui": "DISABLED", "snmp": "DISABLED", "ftp": "DISABLED", "mgmtaccess": "DISABLED", "restrictaccess": "DISABLED", "decrementttl": "DISABLED", "dynamicrouting": "DISABLED", "hostroute": "DISABLED", "advertiseondefaultpartition": "DISABLED", "networkroute": "DISABLED", "tag": "0", "hostrtgwact": "0.0.0.0", "metric": 0, "ospfareaval": "0", "vserverrhilevel": "ONE_VSERVER", "vserverrhimode": "DYNAMIC_ROUTING", "viprtadv2bsd": false, "vipvsercount": "0", "vipvserdowncount": "0", "vipvsrvrrhiactivecount": "0", "vipvsrvrrhiactiveupcount": "0", "ospflsatype": "TYPE5", "state": "ENABLED", "freeports": "1032079", "riserhimsgcode": 0, "iptype": [ "SNIP" ], "icmpresponse": "NONE", "ownernode": "255", "arpresponse": "NONE", "ownerdownresponse": "YES" } ] }root@ubuntu:~#
```

## Load-balancing using Citrix ADC CPX

An example to configure CPX to load-balance HTTP traffic between two Application containers on same Linux host.

   * Pull Application container image on Linux host
   
   ```
   docker pull <image-name>[:<version>]
   ```
   
   * Deploy two Application containers using 'docker run' command
   
   ```
   root@ubuntu:~# docker run -dt --name A1 <image-name>[:<version>]
4688e72bd1eaa669f26310434481766e41f8dad76735c62c7fb2c8f946776230
root@ubuntu:~#
root@ubuntu:~# docker run -dt --name A2 <image-name>[:<version>]
f87bf3770bfe4c557e6cc5c5a26f03669d58a6f2419e8573f9aeb01b6751e540
   ```

   * Finding out the IPs of Application containers using 'docker inspect' command. It will be used for configuring services in CPX.
   
   ```
   root@ubuntu:~# docker inspect A1 | grep IPA
            "SecondaryIPAddresses": null,
            "IPAddress": "172.17.0.7",
                    "IPAMConfig": null,
                    "IPAddress": "172.17.0.7",
root@ubuntu:~#
root@ubuntu:~# docker inspect A2 | grep IPA
            "SecondaryIPAddresses": null,
            "IPAddress": "172.17.0.8",
                    "IPAMConfig": null,
                    "IPAddress": "172.17.0.8",
root@ubuntu:~#
   ```
   
   * Configuring VIP and Services on CPX using **cli_script.sh**.  

   ```
   root@ubuntu:~# docker exec -it cpx-hello-world bash
root@00d58f020a9e:/# cli_script.sh "add lb vserver v1 HTTP 127.0.0.1 10080"
exec: add lb vserver v1 HTTP 127.0.0.1 10080
Done
root@00d58f020a9e:/# cli_script.sh "add service s1 172.17.0.7 HTTP 80"
exec: add service s1 172.17.0.7 HTTP 80
Done
root@00d58f020a9e:/# cli_script.sh "add service s2 172.17.0.8 HTTP 80"
exec: add service s2 172.17.0.8 HTTP 80
Done
root@00d58f020a9e:/# cli_script.sh "bind lb vserver v1 s1"
exec: bind lb vserver v1 s1
Done
root@00d58f020a9e:/# cli_script.sh "bind lb vserver v1 s2"
exec: bind lb vserver v1 s2
Done
root@00d58f020a9e:/# cli_script.sh "stat lb vserver v1"
exec: stat lb vserver v1
Virtual Server Summary
                      vsvrIP  port     Protocol        State   Health  actSvcs
v1                172.17.0.6 10080         HTTP           UP      100        2
           inactSvcs
v1                 0
Virtual Server Statistics
                                          Rate (/s)                Total
Vserver hits                                       0                    0
Requests                                           0                    0
Responses                                          0                    0
Request bytes                                      0                    0
Response bytes                                     0                    0
Total Packets rcvd                                 0                    0
Total Packets sent                                 0                    0
Current client connections                        --                    0
Current Client Est connections                    --                    0
Current server connections                        --                    0
Current Persistence Sessions                      --                    0
Current Backup Persistence Sessi                  --                    0
Requests in surge queue                           --                    0
Requests in vserver's surgeQ                      --                    0
Requests in service's surgeQs                     --                    0
Spill Over Threshold                              --                    0
Spill Over Hits                                   --                    0
Labeled Connection                                --                    0
Push Labeled Connection                           --                    0
Deferred Request                                   0                    0
Invalid Request/Response                          --                    0
Invalid Request/Response Dropped                  --                    0
Vserver Down Backup Hits                          --                    0
Current Multipath TCP sessions                    --                    0
Current Multipath TCP subflows                    --                    0
Apdex for client response times.                  --                 1.00
Average client TTLB                               --                    0
No of TCPConn ReasmQ 75% reached                  --                    0
No of TCPConn ReasmQ Flushed                      --                    0
No of Server Busy Error                            0                    0
s1                172.17.0.7    80         HTTP           UP        0      0/s
s2                172.17.0.8    80         HTTP           UP        0      0/s
Done
root@00d58f020a9e:/#
   ```
   
   * Verify HTTP load-balancing by using curl from Linux host
   
   ```
   root@ubuntu:~# curl http://172.17.0.6:10080
<html><body><h1>It works!</h1></body></html>
root@ubuntu:~#
root@ubuntu:~# curl http://172.17.0.6:10080
<html><body><h1>It works!</h1></body></html>
root@ubuntu:~#
root@ubuntu:~# docker exec -it cpx-hello-world cli_script.sh "stat lb vserver v1"
exec: stat lb vserver v1
Virtual Server Summary
                      vsvrIP  port     Protocol        State   Health  actSvcs
v1                172.17.0.6 10080         HTTP           UP      100        2
           inactSvcs
v1                 0
Virtual Server Statistics
                                          Rate (/s)                Total
Vserver hits                                       0                    2
Requests                                           0                    2
Responses                                          0                    2
Request bytes                                      0                    0
Response bytes                                     0                    0
Total Packets rcvd                                 0                    0
Total Packets sent                                 0                    0
Current client connections                        --                    0
Current Client Est connections                    --                    0
Current server connections                        --                    0
Current Persistence Sessions                      --                    0
Current Backup Persistence Sessi                  --                    0
Requests in surge queue                           --                    0
Requests in vserver's surgeQ                      --                    0
Requests in service's surgeQs                     --                    0
Spill Over Threshold                              --                    0
Spill Over Hits                                   --                    0
Labeled Connection                                --                    0
Push Labeled Connection                           --                    0
Deferred Request                                   0                    0
Invalid Request/Response                          --                    0
Invalid Request/Response Dropped                  --                    0
Vserver Down Backup Hits                          --                    0
Current Multipath TCP sessions                    --                    0
Current Multipath TCP subflows                    --                    0
Apdex for client response times.                  --                 1.00
Average client TTLB                               --                    0
No of TCPConn ReasmQ 75% reached                  --                    0
No of TCPConn ReasmQ Flushed                      --                    0
No of Server Busy Error                            0                    0
s1                172.17.0.7    80         HTTP           UP        1      0/s
s2                172.17.0.8    80         HTTP           UP        1      0/s
Done
root@ubuntu:~#
   ```
   
## More Info about Citrix ADC CPX

Please refer to [CPX Documentation] (https://docs.citrix.com/en-us/citrix-adc-cpx/13/)
