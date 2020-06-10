# Allowlisting or blocklisting IP addresses

**Allowlisting IP addresses** allows you to create a list of trusted IP addresses or IP address ranges from which users can access your domains. It is a security feature that is often used to limit and control access only to trusted users.

**Blocklisting IP addresses** is a basic access control mechanism. It denies access to the users accessing your domain using the IP addresses that you have blocklisted.

The [Rewrite and Responder CRD](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/crds/rewrite-responder/) provided by Citrix enables you to define extensive rewrite and responder policies using datasets, patsets, and string maps and also enable audit logs for statistics on the Ingress Citrix ADC.

Using the rewrite or responder policies you can allowlist or blocklist the IP addresses/CIDR using which users can access your domain.

The following sections cover various ways you can allowlist or blocklist the IP addresses/CIDR using the rewrite or responder policies.

## Allowlist IP addresses

Using a responder policy, you can allowlist IP addresses and silently drop the requests from the clients using IP addresses different from the allowlisted IP addresses.

Create a file named `allowlist-ip.yaml` with the following rewrite policy configuration:

```yml
apiVersion: citrix.com/v1
kind: rewritepolicy
metadata:
  name: allowlistip
spec:
  responder-policies:
    - servicenames:
        - frontend
      responder-policy:
        drop:
        respond-criteria: '!client.ip.src.TYPECAST_text_t.equals_any("allowlistip")'
        comment: 'Allowlist certain IP addresses'
  patset:
    - name: allowlistip
      values:
        - '10.xxx.170.xx'
        - '10.xxx.16.xx'
```

You can also provide the IP addresses as a list:

```yml
apiVersion: citrix.com/v1
kind: rewritepolicy
metadata:
  name: allowlistip
spec:
  responder-policies:
    - servicenames:
        - frontend
      responder-policy:
        drop:
        respond-criteria: '!client.ip.src.TYPECAST_text_t.equals_any("allowlistip")'
        comment: 'Allowlist certain IP addresses'
  patset:
    - name: allowlistip
      values: [ '10.xxx.170.xx', '10.xxx.16.xx' ]
```

Then, deploy the YAML file (`allowlist-ip.yaml`) using the following command:

    kubectl create -f allowlist-ip.yaml

## Allowlist IP addresses and send 403 response to the request from clients not in the allowlist

Using a responder policy, you can allowlist a list of IP addresses and send the `HTTP/1.1 403 Forbidden` response to the requests from the clients using IP addresses different from the allowlisted IP addresses.

Create a file named `allowlist-ip-403.yaml` with the following rewrite policy configuration:

```yml
apiVersion: citrix.com/v1
kind: rewritepolicy
metadata:
  name: allowlistip
spec:
  responder-policies:
    - servicenames:
        - frontend
      responder-policy:
        respondwith:
          http-payload-string: '"HTTP/1.1 403 Forbidden\r\n\r\n" + "Client: " + CLIENT.IP.SRC + " is not authorized to access URL:" + HTTP.REQ.URL.HTTP_URL_SAFE +"\n"'
        respond-criteria: '!client.ip.src.TYPECAST_text_t.equals_any("allowlistip")'
        comment: 'Allowlist a list of IP addresses'
  patset:
    - name: allowlistip
      values: [ '10.xxx.170.xx',  '10.xxx.16.xx' ]
```

Then, deploy the YAML file (`allowlist-ip-403.yaml`) using the following command:

    kubectl create -f allowlist-ip-403.yaml

## Allowlist a CIDR

You can allowlist a CIDR using a responder policy. The following is a sample responder policy configuration to allowlist a CIDR:

```yml
apiVersion: citrix.com/v1
kind: rewritepolicy
metadata:
  name: blocklistips1
spec:
  responder-policies:
    - servicenames:
        - frontend
      responder-policy:
        respondwith:
          http-payload-string: '"HTTP/1.1 403 Forbidden\r\n\r\n" + "Client: " + CLIENT.IP.SRC + " is not authorized to access URL:" + HTTP.REQ.URL.HTTP_URL_SAFE +"\n"'
        respond-criteria: '!client.ip.src.IN_SUBNET(10.xxx.170.xx/24)'
        comment: 'Allowlist certain IPs'
```

## Blocklist IP addresses

Using a responder policy, you can blocklist IP addresses and silently drop the requests from the clients using the blocklisted IP addresses.

Create a file named `blocklist-ip.yaml` with the following responder policy configuration:

```yml
apiVersion: citrix.com/v1
kind: rewritepolicy
metadata:
  name: blocklistips
spec:
  responder-policies:
    - servicenames:
        - frontend
      responder-policy:
        respondwith:
        drop:
        respond-criteria: 'client.ip.src.TYPECAST_text_t.equals_any("blocklistips")'
        comment: 'Blocklist certain IPS'

  patset:
    - name: blocklistips
      values:
        - '10.xxx.170.xx'
        - '10.xxx.16.xx'
```

Then, deploy the YAML file (`blocklist-ip.yaml`) using the following command:

    kubectl create -f blocklist-ip.yaml

## Blocklist a CIDR

You can blocklist a CIDR using a responder policy. The following is a sample responder policy configuration to blocklist a CIDR:

```yml
apiVersion: citrix.com/v1
kind: rewritepolicy
metadata:
  name: blocklistips1
spec:
  responder-policies:
    - servicenames:
        - frontend
      responder-policy:
        respondwith:
          http-payload-string: '"HTTP/1.1 403 Forbidden\r\n\r\n" + "Client: " + CLIENT.IP.SRC + " is not authorized to access URL:" + HTTP.REQ.URL.HTTP_URL_SAFE +"\n"'
        respond-criteria: 'client.ip.src.IN_SUBNET(10.xxx.170.xx/24)'
        comment: 'Blocklist certain IPs'
```

## Allowlist a CIDR and blocklist IP addresses

You can allowlist a CIDR and also blocklist IP addresses using a responder policy. The following is a sample responder policy configuration:

```yml
apiVersion: citrix.com/v1
kind: rewritepolicy
metadata:
  name: allowlistsub
spec:
  responder-policies:
    - servicenames:
        - frontend
      responder-policy:
        drop:
        respond-criteria: 'client.ip.src.TYPECAST_text_t.equals_any("blocklistips") || !client.ip.src.IN_SUBNET(10.xxx.170.xx/24)'
        comment: 'Allowlist a subnet and blocklist few IP's'

  patset:
    - name: blocklistips
      values:
        - '10.xxx.170.xx'
```

## Blocklist a CIDR and allowlist IP addresses

You can blocklist a CIDR and also allowlist IP addresses using a responder policy. The following is a sample responder policy configuration:

```yml
apiVersion: citrix.com/v1
kind: rewritepolicy
metadata:
  name: blocklistips1
spec:
  responder-policies:
    - servicenames:
        - frontend
      responder-policy:
        drop:
        respond-criteria: 'client.ip.src.IN_SUBNET(10.xxx.170.xx/24) && !client.ip.src.TYPECAST_text_t.equals_any("allowlistips")'
        comment: 'Blocklist a subnet and allowlist few IP's'

  patset:
    - name: allowlistips
      values:
        - '10.xxx.170.xx'
        - '10.xxx.16.xx'
```