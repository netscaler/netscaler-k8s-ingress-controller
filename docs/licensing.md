# Licensing

For licensing the Citrix ADC CPX, you need to provide the following information in the YAML for the Citrix Application Delivery Management (ADM) to automatically pick the licensing information:

-  **LS_IP (License server IP)** – Specify the Citrix ADM IP address.

-  **LS_PORT (License server Port)** – This is not a mandatory field. You must specify the ADM port only if you have changed it. The default port is 27000.

-  **PLATFORM** – Specify the Platform License. Platform is **CP1000**.

The following is a sample yaml file:

```yml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: cpx-ingress
  labels:
    name: cpx-ingress
spec:
  replicas: 1
  selector:
    matchLabels:
      name: cpx-ingress
  template:
    metadata:
      labels:
        name: cpx-ingress
      annotations:
        NETSCALER_AS_APP: "True"
    spec:
      serviceAccountName: cpx
      containers:
        - name: cpx-ingress
          image: "cpx-ingress:latest"
          securityContext:
            privileged: true
          env:
            - name: "EULA"
              value: "YES"
            - name: "NS_PROTOCOL"
              value: "HTTP"
            #Define the NITRO port here
            - name: "NS_PORT"
              value: "9080"
            - name: "LS_IP"
              value: "<ADM IP>"
            - name: "LS_PORT"
              value: "27000"
            - name: "PLATFORM"
              value: "CP1000"
          args:
            - --ingress-classes
              citrix-ingress
          ports:
            - name: http
              containerPort: 80
            - name: https
              containerPort: 443
            - name: nitro-http
              containerPort: 9080
            - name: nitro-https
              containerPort: 9443
          imagePullPolicy: Always
```