# Enable gRPC support using the Citrix ingress controller

gRPC is a high performance, open-source universal RPC framework created by Google. In gRPC, a client application can directly call methods on a server application from a different server in the same way you call local methods.
You can easily create distributed applications and services using GRPC.

## Enable gRPC support

Perform the following steps to enable GRPC support using HTTP2.

1. Create a YAML file `cic-configmap.yaml` and enable the global parameter for HTTP2 server side support using the following entry in the ConfigMap. For more information on using ConfigMap, see the [ConfigMap documentation](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/configure/config-map/).

           NS_HTTP2_SERVER_SIDE: 'ON'

2. Apply the ConfigMap using the following command.

           kubectl apply -f cic-configmap.yaml

3. Edit the `cic.yaml` file for deploying the Citrix ingress controller to support ConfigMap.

        
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: cic-k8s-ingress-controller
        spec:
          selector:
            matchLabels:
              app: cic-k8s-ingress-controller
          replicas: 1
          template:
            metadata:
              name: cic-k8s-ingress-controller
              labels:
                app: cic-k8s-ingress-controller
              annotations:
            spec:
              serviceAccountName: cic-k8s-role
              containers:
              - name: cic-k8s-ingress-controller
                image: "quay.io/citrix/citrix-k8s-ingress-controller:1.8.19"
                env:
                # Set NetScaler NSIP/SNIP, SNIP in case of HA (mgmt has to be enabled)
                - name: "NS_IP"
                  value: "10.106.143.133"
                # Set username for Nitro
                - name: "NS_USER"
                  valueFrom:
                    secretKeyRef:
                    name: nslogin
                    key: username
                # Set user password for Nitro
                - name: "NS_PASSWORD"
                  valueFrom:
                    secretKeyRef:
                    name: nslogin
                    key: password
                # Set log level
                - name: "EULA"
                  value: "yes"
                envFrom:
                - configMapRef:
                    name: cic-configmap
                args:
                  - --ingress-classes
                    citrix
                  - --feature-node-watch
                    true
                  - --default-ssl-certificate
                    default/default.secret
                  - --configmap
                    default/cic-configmap
                # imagePullPolicy: IfNotPresent
                imagePullPolicy: Always

4. Deploy the Citrix ingress controller as a stand-alone pod by applying the edited YAML file.

        kubectl apply -f cic.yaml

5. To test the gRPC traffic, you may need to install `grpcurl`. Perform the following steps to install `grpcurl` on a Linux machine.

        go get github.com/fullstorydev/grpcurl
        go install github.com/fullstorydev/grpcurl/cmd/grpcurl

6. Apply the gRPC test service YAML file (`grpc-service.yaml`).

        kubectl apply -f grpc-service.yaml

    Following is a sample content for the `grpc-service.yaml` file. 
         

          apiVersion: apps/v1
          kind: Deployment
          metadata:
            name: grpc-service
          spec:
            replicas: 1
            selector:
              matchLabels:
                app: grpc-service
            template:
              metadata:
                labels:
                  app: grpc-service
              spec:
                containers:
                - image: registry.cn-hangzhou.aliyuncs.com/acs-sample/grpc-server:latest
                  imagePullPolicy: Always
                  name: grpc-service
                  ports:
                  - containerPort: 50051
                    protocol: TCP
                restartPolicy: Always
          ---
          apiVersion: v1
          kind: Service
          metadata:
            name: grpc-service
          spec:
            ports:
            - port: 50051
              protocol: TCP
              targetPort: 50051
            selector:
              app: grpc-service
            sessionAffinity: None
            type: NodePort

7. Create a certificate for the gRPC Ingress configuration.

        openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt -subj "/CN=grpc.example.com/O=grpc.example.com"
       
        kubectl create secret tls grpc-secret --key tls.key --cert tls.crt

        secret "grpc-secret" created

8. Enable HTTP2 using Ingress annotations. See [HTTP/2 support](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/how-to/http-use-cases.md) for steps to enable HTTP2 using the Citrix ingress controller.

   - Create a YAML file for the front-end Ingress configuration and apply it to enable HTTP/2 on the content switching virtual server.
  
          kubectl apply -f frontend-ingress.yaml
  
     The content of the `frontend-ingress.yaml` file is provided as follows:

          apiVersion: networking.k8s.io/v1
          kind: Ingress
          metadata:
            annotations:
              ingress.citrix.com/frontend-httpprofile: '{"http2":"enabled", "http2direct" : "enabled"}'
              ingress.citrix.com/frontend-ip: 192.0.2.1
              ingress.citrix.com/secure-port: "443"
              kubernetes.io/ingress.class: citrix
            name: frontend-ingress
          spec:
            rules:
            - {}
            tls:
            - {}

   - Create a YAML file for the back-end Ingress configuration with the following content and apply it to enable HTTP2 on back-end (service group).

          kubectl apply -f backend-ingress.yaml

      The content of the `backend-ingress.yaml` file is provided as follows:

          apiVersion: networking.k8s.io/v1
          kind: Ingress
          metadata:
            annotations:
              ingress.citrix.com/backend-httpprofile: '{"grpc-service":{"http2": "enabled", "http2direct" : "enabled"}}'
              ingress.citrix.com/frontend-ip: 192.0.2.2
              ingress.citrix.com/secure-port: "443"
              kubernetes.io/ingress.class: citrix
            name: grpc-ingress
          spec:
            rules:
            - host: grpc.example.com
              http:
                paths:
                - backend:
                    service:
                      name: grpc-service
                      port:
                        number: 50051
                  path: /
                  pathType: Prefix
            tls:
            - hosts:
              - grpc.example.com
              secretName: grpc-secret

3. Test the gRPC traffic using the `grpcurl` command.


        grpcurl -v -insecure -d '{"name": "gRPC"}' grpc.example.com:443 helloworld.Greeter.SayHello

    The output of the command is shown as follows:

        Resolved method descriptor:
        rpc SayHello ( .helloworld.HelloRequest ) returns ( .helloworld.HelloReply );
 
 
        Request metadata to send:
        (empty)
 
 
        Response headers received:
        content-type: application/grpc
 

        Response contents:
        {
            "message": "Hello gRPC"
        }
 
 
        Response trailers received:
        (empty)
        Sent 1 request and received 1 response

## Validate the rate limit CRD

Perform the following steps to validate the rate limit CRD.

1. Apply the rate limit CRD using the [ratelimit-crd.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/crd/ratelimit/ratelimit-crd.yaml) file.

       kubectl create -f ratelimit-crd.yaml

2. Create a YAML file (ratelimit-crd-object.yaml) with the following content for the rate limit policy.


          apiVersion: citrix.com/v1beta1
          kind: ratelimit
          metadata:
            name: throttle-req-per-clientip
          spec:
            servicenames:
              - grpc-service
            selector_keys:
            basic:
              path:
              - "/"
              per_client_ip: true
            req_threshold: 5
            timeslice: 60000
            throttle_action: "RESPOND"
         

1. Apply the YAML file using the following command.
  
          kubectl create -f ratelimit-crd-object.yaml

2. Test gRPC traffic using the `grpcurl` command.


        grpcurl -v -insecure -d '{"name": "gRPC"}' grpc.example.com:443 helloworld.Greeter.SayHello

      The command returns the following error in response after the rate limit is reached:

        Error invoking method "helloworld.Greeter.SayHello": failed to query for service descriptor "helloworld.Greeter": rpc error: code = Unavailable desc =

        Too Many Requests: HTTP status code 429; transport: missing content-type field

## Validate the Rewrite and Responder CRD with gRPC

Perform the following steps to validate the Rewrite and Responder CRD.

1. Apply the Rewrite and Responder CRD using the [rewrite-responder-policies-deployment.yaml](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/crd/rewrite-responder-policies-deployment.yaml) file.

       kubectl create -f rewrite-responder-policies-deployment.yaml

2. Create a YAML file (rewrite-crd-object.yaml) with the following content for the rewrite policy.

      
        apiVersion: citrix.com/v1
        kind: rewritepolicy
        metadata:
          name: addcustomheaders
        spec:
          rewrite-policies:
            - servicenames:
                - grpc-service
              rewrite-policy:
                operation: insert_http_header
                target: 'sessionID'
                modify-expression: '"48592th42gl24456284536tgt2"'
                comment: 'insert SessionID in header'
                direction: RESPONSE
                rewrite-criteria: 'http.res.is_valid'


1. Apply the YAML file using the following command. 

        kubectl create -f rewrite-crd-object.yaml

3. Test the gRPC traffic using the `grpcurl` command.

        grpcurl -v -insecure -d '{"name": "gRPC"}' grpc.example.com:443 helloworld.Greeter.SayHello

    
     This command adds a session id in the gRPC request response.

        Resolved method descriptor:
        rpc SayHello ( .helloworld.HelloRequest ) returns ( .helloworld.HelloReply );

        Request metadata to send:
        (empty)

        Response headers received:
        content-type: application/grpc
        sessionid: 48592th42gl24456284536tgt2

        Response contents:
        {
          "message": "Hello gRPC"
        }

        Response trailers received:
        (empty)
        Sent 1 request and received 1 response