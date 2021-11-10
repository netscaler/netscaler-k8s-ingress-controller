from collections import OrderedDict

class rbac:
    '''
       Class for Creating RBAC for CIC
    '''

    def __init__(self):
        self.name = "citrix"

    def createRbac(self):
        '''
            Function to create RBAC for CIC
        '''

        self.clusterRole = self.createClusterRole()
        self.clusterRoleBinding = self.createClusterRoleBinding()
        self.serviceAccount = self.createServiceAccount()

        # Concatenating all the yamls
        self.yaml = [self.clusterRole, self.clusterRoleBinding, self.serviceAccount]

        return(self.yaml)


    def createClusterRole(self):
        '''
           Function to Create ClusterRole
        '''

        basicConfigIn = OrderedDict([
        ("apiVersion", "rbac.authorization.k8s.io/v1"),
        ("kind", "ClusterRole"),
        ("metadata", {
            "name": "%s" % (self.name),
        }),
        ("rules", [
           {
           "apiGroups": [""],
           "resources": ["endpoints", "ingresses", "pods", "secrets", "nodes", "routes", "namespaces","configmaps"],
           "verbs": ["get", "list", "watch"],
           },
           {
           "apiGroups": [""],
           "resources": ["services/status"],
           "verbs": ["patch"],
           },
           {
           "apiGroups": [""],
           "resources": ["services"],
           "verbs": ["get", "list", "watch", "patch"],
           },
           {
           "apiGroups": [""],
           "resources": ["events"],
           "verbs": ["create"],
           },
           {
           "apiGroups": ["extensions"],
           "resources": ["ingresses", "ingresses/status"],
           "verbs": ["get", "list", "watch"],
           },
           {
           "apiGroups": ["apiextensions.k8s.io"],
           "resources": ["customresourcedefinitions"],
           "verbs": ["get", "list", "watch"],
           },
           {
           "apiGroups": ["apps"],
           "resources": ["deployments"],
           "verbs": ["get", "list", "watch"],
           },
           {
           "apiGroups": ["citrix.com"],
           "resources": ["rewritepolicies", "canarycrds", "authpolicies", "ratelimits", "listeners","httproutes"],
           "verbs": ["get", "list", "watch"],
           },
           {
           "apiGroups": ["citrix.com"],
           "resources": ["rewritepolicies/status", "canarycrds/status", "authpolicies/status", "ratelimits/status", "listeners/status","httproutes/status"],
           "verbs": ["get", "list", "patch"],
           },
           {
           "apiGroups": ["citrix.com"],
           "resources": ["vips"],
           "verbs": ["get", "list", "watch", "create", "delete"],
           },
           {
           "apiGroups": ["route.openshift.io"],
           "resources": ["routes"],
           "verbs": ["get", "list", "watch"],
           },
        ])
        ])

        return(basicConfigIn)

    def createClusterRoleBinding(self):
        '''
           Function to Create RBAC ClusterRoleBinding
        '''

        basicConfigIn = OrderedDict([
        ("apiVersion", "rbac.authorization.k8s.io/v1"),
        ("kind", "ClusterRoleBinding"),
        ("metadata", {
            "name": "%s" % (self.name),
        }),
        ("roleRef", {
            "apiGroup": "rbac.authorization.k8s.io",
            "kind": "ClusterRole",
            "name": "%s" % (self.name),
        }),
        ("subjects", [
            {
                "kind": "ServiceAccount",
                "name": "%s" % (self.name),
                "namespace": "default",
            },
        ])
        ])

        return(basicConfigIn)

    def createServiceAccount(self):
        '''
           Function to Create RBAC ServiceAccount
        '''

        basicConfigIn = OrderedDict([
        ("apiVersion", "v1"),
        ("kind", "ServiceAccount"),
        ("metadata", {
            "name": "%s" % (self.name),
            "namespace": "default",
        })
        ]) 

        return(basicConfigIn)

class cpxCic:
    '''
        Class for Creating a CPX+CIC yaml manifest file
    '''

    def __init__(self, cpxCicInput={}):
        self.name = cpxCicInput["name"]
        self.cicContainerName = "cic"
        self.cpxContainerName = "cpx"
        self.cpxImage = "quay.io/citrix/citrix-k8s-cpx-ingress:13.0-83.27"
        self.cicImage = "quay.io/citrix/citrix-k8s-ingress-controller:1.19.6"
        self.imagePullPolicy = "Always"
        self.readinessProbe = True
        self.serviceAccountName = "citrix"
        self.rbacNeeded = True # Disable this flag if you don't need RBAC
        self.exposeService = True
        self.cpxSecretRequired = True
        self.externalTrafficPolicy = None # Set this to 'None' so that this flag is not set
        self.serviceType = None
        if "ingressClass" in cpxCicInput.keys():
            self.ingressClass = cpxCicInput["ingressClass"]

    def create(self):
        '''
           Function to create the YAML Manifest
        '''

        basicConfigIn = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": "%s" % (self.name),
        },
        "spec": {
            "replicas": 1,
            "selector": {
                "matchLabels": {
                    "app": "%s" % (self.name)
                },
            },
            "template": {
                "metadata": {
                    "name": "%s" % (self.name),
                    "labels": {
                        "app": "%s" % (self.name),
                    },
                },
                "spec": {
                    "serviceAccountName": "%s" % (self.serviceAccountName),
                    "containers": [],
                },
            },
        },
        }

        if self.exposeService:
            self.exposedPorts = [80, 443, 9080, 9443]
            self.serviceType = "ClusterIP"
            self.serviceManifest = self.createCpxService()

        if self.cpxSecretRequired:
            self.secretManifest = self.createCPXSecret()

        # Store the manifests to the Object
        self.manifest = []
        self.skeletonManifest = basicConfigIn

        self.cpxManifest = self.createCpxSpec()
        self.cicManifest = self.createCicSpec()

        basicConfigIn['spec']['template']['spec']['containers'].append(self.cpxManifest)
        basicConfigIn['spec']['template']['spec']['containers'].append(self.cicManifest)

        self.manifest.append(basicConfigIn)

        if self.exposeService:
           self.manifest.append(self.serviceManifest)

        if self.cpxSecretRequired:
            self.manifest.append(self.secretManifest)

        return(self.manifest)

    def createCpxSpec(self):
        '''
            Function to create the Spec for CPX Container
        '''

        basicConfigIn = {
        "name": "%s" % (self.cpxContainerName),
        "image": "%s" % (self.cpxImage),
        "imagePullPolicy": "%s" % (self.imagePullPolicy),
        "securityContext":{"privileged": True},
        "env":[
            {"name": "EULA", "value": "yes"},
            {"name": "KUBERNETES_TASK_ID", "value": ""}, 
        ],
        "ports":[
            {"name": "http", "containerPort": 80},
            {"name": "https", "containerPort": 443},
            {"name": "nitro-http", "containerPort": 9080},
            {"name": "nitro-https", "containerPort": 9443},
        ],
        }

        # Add readinessProbe to CPX if enabled - By Default this is needed for Cloud Deployments
        if self.readinessProbe:
            readinessProbeConfigIn = {
                "tcpSocket": {"port": 9080},
                "initialDelaySeconds": 60,
                "periodSeconds": 5,
                "failureThreshold": 5,
                "successThreshold": 1,
            }
            basicConfigIn['readinessProbe'] = readinessProbeConfigIn

        return(basicConfigIn)

    def createCicSpec(self):
        '''
           Function to Create a Spec for the CIC container
        '''

        basicConfigIn = {
        "name": "%s" % (self.cicContainerName),
        "image": "%s" % (self.cicImage),
        "imagePullPolicy": "%s" % (self.imagePullPolicy),
        "env":[
            {"name": "EULA", "value": "yes"},
            {"name": "NS_IP", "value": "127.0.0.1"},
            {"name": "NS_PROTOCOL", "value": "HTTP"},
            {"name": "NS_PORT", "value": "80"},
            {"name": "NS_DEPLOYMENT_MODE", "value": "SIDECAR"},
            {"name": "NS_ENABLE_MONITORING", "value": "YES"},
            {"name": "NS_USER", "valueFrom": {"secretKeyRef": {"name": self.name, "key":"username"}}},
            {"name": "NS_PASSWORD", "valueFrom": {"secretKeyRef": {"name": self.name, "key":"password"}}},
            {"name": "POD_NAME", "valueFrom": {"fieldRef": {"apiVersion": "v1", "fieldPath":"metadata.name"}}},
            {"name": "POD_NAMESPACE", "valueFrom": {"fieldRef": {"apiVersion": "v1", "fieldPath":"metadata.namespace"}}},
        ],
        "args": [],
        }

        if self.ingressClass is not None:
            basicConfigIn['args'].append("--ingress-classes %s" % self.ingressClass)

        return(basicConfigIn)

    def createCpxService(self):
        '''	
           Function to create service for CPX using Type LoadBalancer
           This is mainly for Cloud Deployments
        '''

        basicConfigIn = {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {"name": self.name},
            "spec": {
                "ports": [],
                "selector": {"app": self.name},
            }
        }

        if self.externalTrafficPolicy:
            basicConfigIn['spec']['externalTrafficPolicy'] = self.externalTrafficPolicy

        if self.serviceType:
            basicConfigIn['spec']['type'] = self.serviceType

        for port in self.exposedPorts:
            basicConfigIn['spec']['ports'].append({"name": "port-"+str(port), "port": port, "targetPort": port})

        self.serviceManifest = basicConfigIn
        return(self.serviceManifest)

    def createCPXSecret(self):
        '''
           Function to create secret for CPX credentials
        '''
        basicConfigIn = {
            "apiVersion": "v1",
            "kind": "Secret",
            "metadata": {
                "name": self.name,
            },
            "type": "Opaque",
            "data": {
                "username": "bnNyb290",
                "password": "bnNyb290",
            }
        }

        self.secretManifest = basicConfigIn
        return(self.secretManifest)

class ingress:
    '''
       Class to create an Ingress Resource
    '''

    def __init__(self, ingressInput={}):
        if ingressInput: 
            self.name = ingressInput["name"] # Name of the Ingress Object
            self.namespace = ingressInput["namespace"] if 'namespace' in ingressInput.keys() else "" 
            self.annotations = dict()
            self.protocol = ingressInput["protocol"]
            self.tls = ingressInput["tls"]
            self.serviceDetails = ingressInput["serviceDetails"]
            self.adm = False
            if "admRequired" in ingressInput.keys():
                if ingressInput["admRequired"]:
                    self.adm = True
#            if "port" in ingressInput.keys():
#                self.tcpPort = ingressInput["port"]
            if "ingressClass" in ingressInput.keys():
                self.ingressClass = ingressInput["ingressClass"]
            else:
                self.ingressClass = None

        # Call create here itself
        self.create()

        

    def create(self):
        '''
           Function to create the Ingress Resource

           sampleInput = {
           # Multiple paths under an hostname
           "hostname1": [
               {"path":"path1","serviceName":"service1","servicePort":port1},
               {"path":"path2","serviceName":"service2","servicePort":port2},
           ],
           # Hostname with single path
           "hostname2": [
               {"path":"path1","serviceName":"service1","servicePort":port1}
           ],
           }

        '''

        basicConfigIn = OrderedDict([
            ("apiVersion", "extensions/v1beta1"),
            ("kind", "Ingress"),
            ("metadata", {
                "name": "%s" % (self.name),
                # TODO: Handle annotations in a better way
                "annotations": self.annotations,
            }),
            ("spec", {})
            ])

#        basicConfigIn['metadata']['annotations']["ingress.citrix.com/insecure-termination"] = 'allow'
        if self.adm:
            basicConfigIn['metadata']['annotations']['ingress.citrix.com/analyticsprofile'] = '{"webinsight": {"httpurl":"ENABLED", "httpuseragent":"ENABLED", "httphost":"ENABLED", "httpmethod":"ENABLED", "httpcontenttype":"ENABLED"}, "tcpinsight": {"tcpBurstReporting":"DISABLED"}}'
        if self.protocol == "tcp":
            basicConfigIn['metadata']['annotations']['ingress.citrix.com/insecure-service-type'] = "tcp"
            basicConfigIn['metadata']['annotations']['ingress.citrix.com/insecure-port'] = self.serviceDetails['servicePort']
        elif self.protocol == "udp":
            basicConfigIn['metadata']['annotations']['ingress.citrix.com/insecure-service-type'] = "udp"
            basicConfigIn['metadata']['annotations']['ingress.citrix.com/insecure-port'] = self.serviceDetails['servicePort']
        elif self.protocol == "http":
            basicConfigIn['metadata']['annotations']['ingress.citrix.com/insecure-service-type'] = "http"
            basicConfigIn['metadata']['annotations']['ingress.citrix.com/insecure-port'] = list(self.serviceDetails.values())[0][0]['servicePort']
        elif self.protocol == "https":
            basicConfigIn['metadata']['annotations']['ingress.citrix.com/secure-backend'] = '{\"'+list(self.serviceDetails.values())[0][0]['serviceName']+'\": \"True\"}'
            basicConfigIn['metadata']['annotations']['ingress.citrix.com/secure-port'] = list(self.serviceDetails.values())[0][0]['servicePort']

        if self.namespace:
            basicConfigIn['metadata']['namespace'] = self.namespace

        if self.ingressClass is not None:
            basicConfigIn['metadata']['annotations']['kubernetes.io/ingress.class'] = self.ingressClass

        if self.tls:
            tlsConfig = [{"secretName": self.tls}]

            basicConfigIn['spec']['tls'] = tlsConfig

        basicConfigIn['spec']['rules'] = []
        # Creating rule and paths for the inputs passed
        if self.protocol == "tcp" or self.protocol == "udp":
            path = self.createPath(self.serviceDetails['serviceName'], self.serviceDetails['servicePort'])
            basicConfigIn['spec'] = path
        else:
            for hostname, paths in self.serviceDetails.items():
                rule = self.createRule(hostname, paths)
                basicConfigIn['spec']['rules'].append(rule)

        return(basicConfigIn)

    def createRule(self, hostname, paths):
        '''
           Function to create an Ingress Rule
           Input Args:
               hostname    - Hostname for the Ingress Rule
               path        - Path for the Ingress Rule
               serviceName - Name of the Kubernetes Service to load-balance
               servicePort - Port of the Kubernetes Service to load-balance
        '''

        basicConfigIn = {
            "host": "%s" % (hostname),
            "http": {
                "paths": [],
            }
        }

        for path in paths:
            out = self.createPath(path['serviceName'], path['servicePort'])
            basicConfigIn['http']['paths'].append(out)

        self.manifest = basicConfigIn
        return(self.manifest)

    def createPath(self, serviceName, servicePort):
        '''
           Function to create an Ingres Path
        '''

        basicConfigIn = {
            "backend": {
                "serviceName": serviceName,
                "servicePort": int(servicePort),
            }
        }

        return(basicConfigIn)

class service:
    '''
       Class to create services

    '''

    def __init__(self, serviceInput={}):

        if serviceInput:
            self.name = serviceInput['name']
            self.namespace = serviceInput['namespace'] if "namespace" in serviceInput.keys() else ""
            self.appLabel = serviceInput['appLabel']
            self.ports = serviceInput["ports"]
            

    def create(self):
        '''
           Function to create service for the deployment
        '''
        
        basicConfigIn = OrderedDict([
            ("apiVersion", "v1"),
            ("kind", "Service"),
            ("metadata", {
                "name": self.name,
                "labels": {"citrix-adc": "cpx"},
            }),
            ("spec", {
                "ports": [],
                "selector": {"app": self.appLabel},
            })
        ])

        for port in self.ports:
            if "name" in port.keys():
                basicConfigIn['spec']['ports'].append({"name":port["name"], "port": port["port"], "targetPort": port["port"]})
            else:
                basicConfigIn['spec']['ports'].append({"port": port["port"], "targetPort": port["port"]})

        if self.namespace:
            basicConfigIn["metadata"]["namespace"] = self.namespace
        self.serviceManifest = basicConfigIn
        return(self.serviceManifest)

