# Licensing

For licensing the Citrix ADC CPX, you need to provide the following information in the YAML for the Citrix Application Delivery Management (ADM) to automatically pick the licensing information:

-  **LS_IP (License server IP)** – Specify the Citrix ADM IP address.

-  **LS_PORT (License server Port)** – This is not a mandatory field. You must specify the ADM port only if you have changed it. The default port is 27000.

-  **PLATFORM** – Specify the Platform License. Platform is **CP1000**.

The following is a sample yaml file:

```yml
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    name: cpx-ingress
  name: cpx-ingress
spec:
  replicas: 1
  selector:
    matchLabels:
      name: cpx-ingress
  template:
    metadata:
      annotations:
        NETSCALER_AS_APP: "True"
      labels:
        name: cpx-ingress
    spec:
      serviceAccountName: cpx
      containers:
      - args:
        - --ingress-classes citrix-ingress
        env:
        - name: EULA
          value: "YES"
        - name: NS_PROTOCOL
          value: HTTP
        - name: NS_PORT
          value: "9080"
        - name: LS_IP
          value: <ADM IP>
        - name: LS_PORT
          value: "27000"
        - name: PLATFORM
          value: CP1000
        image: cpx-ingress:latest
        imagePullPolicy: Always
        name: cpx-ingress
        ports:
        - containerPort: 80
          name: http
          protocol: TCP
        - containerPort: 443
          name: https
          protocol: TCP
        - containerPort: 9080
          name: nitro-http
          protocol: TCP
        - containerPort: 9443
          name: nitro-https
          protocol: TCP
        securityContext:
          privileged: true
```