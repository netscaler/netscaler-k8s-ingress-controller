# Whitelisting or Blacklisting IP addresses

**Whitelisting IP addresses** allows you to create a list of trusted IP addresses or IP address ranges from which users can access your domains. It is a security feature that is often used to limit and control access only to trusted users.

**Blacklisting IP addresses** is a basic access control mechanism. It denies access to the users accessing your domain using the IP addresses that you have blacklisted.

The [Rewrite and Responder CRD](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/crds/rewrite-responder/) provided by Citrix enables you to define extensive rewrite and responder policies using datasets, patsets, and string maps and also enable audit logs for statistics on the Ingress Citrix ADC.

Using the rewrite or responder policies you can whitelist or blacklist the IP addresses/CIDR using which users can access your domain.

The following sections cover various ways you can whitelist or blacklist the IP addresses/CIDR using the rewrite or responder policies.

## Whitelist IP addresses

Using a responder policy, you can whitelist IP addresses and silently drop the requests from the clients using IP addresses different from the whitelisted IP addresses.

Create a file named `whitelist-ip.yaml` with the following rewrite policy configuration:

```yml
apiVersion: citrix.com/v1
kind: rewritepolicy
metadata:
  name: whitelistip
spec:
  responder-policies:
    - servicenames:
        - frontend
      responder-policy:
        drop:
        respond-criteria: '!client.ip.src.TYPECAST_text_t.equals_any("whitelistip")'
        comment: 'Whitelist certain IP addresses'
  patset:
    - name: whitelistip
      values:
        - '10.xxx.170.xx'
        - '10.xxx.16.xx'
```

You can also provide the IP addresses as a list:

```yml
apiVersion: citrix.com/v1
kind: rewritepolicy
metadata:
  name: whitelistip
spec:
  responder-policies:
    - servicenames:
        - frontend
      responder-policy:
        drop:
        respond-criteria: '!client.ip.src.TYPECAST_text_t.equals_any("whitelistip")'
        comment: 'Whitelist certain IP addresses'
  patset:
    - name: whitelistip
      values: [ '10.xxx.170.xx', '10.xxx.16.xx' ]
```

Then, deploy the YAML file (`whitelist-ip.yaml`) using the following command:

    kubectl create -f whitelist-ip.yaml

## Whitelist IP addresses and send 403 response to the request from clients not in the whitelist

Using a responder policy, you can whitelist a list of IP addresses and send `HTTP/1.1 403 Forbidden` response to the requests from the clients using IP addresses different from the whitelisted IP addresses.

Create a file named `whitelist-ip-403.yaml` with the following rewrite policy configuration:

```yml
apiVersion: citrix.com/v1
kind: rewritepolicy
metadata:
  name: whitelistip
spec:
  responder-policies:
    - servicenames:
        - frontend
      responder-policy:
        respondwith:
          http-payload-string: '"HTTP/1.1 403 Forbidden\r\n\r\n" + "Client: " + CLIENT.IP.SRC + " is not authorized to access URL:" + HTTP.REQ.URL.HTTP_URL_SAFE +"\n"'
        respond-criteria: '!client.ip.src.TYPECAST_text_t.equals_any("whitelistip")'
        comment: 'Whitelist a list of IP addresses'
  patset:
    - name: whitelistip
      values: [ '10.xxx.170.xx',  '10.xxx.16.xx' ]
```

Then, deploy the YAML file (`whitelist-ip-403.yaml`) using the following command:

    kubectl create -f whitelist-ip-403.yaml

## Whitelist a CIDR

You can whitelist a CIDR using a responder policy. The following is a sample responder policy configuration to whitelist a CIDR:

```yml
apiVersion: citrix.com/v1
kind: rewritepolicy
metadata:
  name: blacklistips1
spec:
  responder-policies:
    - servicenames:
        - frontend
      responder-policy:
        respondwith:
          http-payload-string: '"HTTP/1.1 403 Forbidden\r\n\r\n" + "Client: " + CLIENT.IP.SRC + " is not authorized to access URL:" + HTTP.REQ.URL.HTTP_URL_SAFE +"\n"'
        respond-criteria: '!client.ip.src.IN_SUBNET(10.xxx.170.xx/24)'
        comment: 'Whitelist certain IPs'
```

## Blacklist IP addresses

Using a responder policy, you can blacklist IP addresses and silently drop the requests from the clients using the blacklisted IP addresses.

Create a file named `blacklist-ip.yaml` with the following responder policy configuration:

```yml
apiVersion: citrix.com/v1
kind: rewritepolicy
metadata:
  name: blacklistips
spec:
  responder-policies:
    - servicenames:
        - frontend
      responder-policy:
        respondwith:
        drop:
        respond-criteria: 'client.ip.src.TYPECAST_text_t.equals_any("blacklistips")'
        comment: 'Blacklist certain IPS'

  patset:
    - name: blacklistips
      values:
        - '10.xxx.170.xx'
        - '10.xxx.16.xx'
```

Then, deploy the YAML file (`blacklist-ip.yaml`) using the following command:

    kubectl create -f blacklist-ip.yaml

## Blacklist a CIDR

You can blacklist a CIDR using a responder policy. The following is a sample responder policy configuration to blacklist a CIDR:

```yml
apiVersion: citrix.com/v1
kind: rewritepolicy
metadata:
  name: blacklistips1
spec:
  responder-policies:
    - servicenames:
        - frontend
      responder-policy:
        respondwith:
          http-payload-string: '"HTTP/1.1 403 Forbidden\r\n\r\n" + "Client: " + CLIENT.IP.SRC + " is not authorized to access URL:" + HTTP.REQ.URL.HTTP_URL_SAFE +"\n"'
        respond-criteria: 'client.ip.src.IN_SUBNET(10.xxx.170.xx/24)'
        comment: 'Blacklist certain IPs'
```

## Whitelist a CIDR and blacklist IP addresses

You can whitelist a CIDR and also blacklist IP addresses using a responder policy. The following is a sample responder policy configuration:

```yml
apiVersion: citrix.com/v1
kind: rewritepolicy
metadata:
  name: whitelistsub
spec:
  responder-policies:
    - servicenames:
        - frontend
      responder-policy:
        drop:
        respond-criteria: 'client.ip.src.TYPECAST_text_t.equals_any("blacklistips") || !client.ip.src.IN_SUBNET(10.xxx.170.xx/24)'
        comment: 'Whitelist a subnet and blacklist few IP's'

  patset:
    - name: blacklistips
      values:
        - '10.xxx.170.xx'
```

## Blacklist a CIDR and whitelist IP addresses

You can blacklist a CIDR and also whitelist IP addresses using a responder policy. The following is a sample responder policy configuration:

```yml
apiVersion: citrix.com/v1
kind: rewritepolicy
metadata:
  name: blacklistips1
spec:
  responder-policies:
    - servicenames:
        - frontend
      responder-policy:
        drop:
        respond-criteria: 'client.ip.src.IN_SUBNET(10.xxx.170.xx/24) && !client.ip.src.TYPECAST_text_t.equals_any("whitelistips")'
        comment: 'Blacklist a subnet and whitelist few IP's'

  patset:
    - name: whitelistips
      values:
        - '10.xxx.170.xx'
        - '10.xxx.16.xx'
```