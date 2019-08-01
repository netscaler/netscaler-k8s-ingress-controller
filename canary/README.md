# Deploy Citrix ADC-Integrated Canary Deployment Solution (**Beta**)

>**IMPORTANT**
>This is the beta version of the solution which is still undergoing final testing before its official release.

## Contents

  +  [Software Requirements](#software-requirements)
  +  [Workflow of a Spinnaker pipeline for Citrix ADC Integrated Canary Deployment Solution](#workflow-of-a-spinnaker-pipeline-for-citrix-adc-integrated-canary-deployment-solution)
  +  [Limitations](#limitations)
  +  [Deploy the Citrix ADC Integrated Canary Deployment Solution in Google cloud Platform](#deploy-the-citrix-adc-integrated-canary-deployment-solution-in-google-cloud-platform)
  +  [Troubleshooting](#troubleshooting)
  +  [Sample JSON file](#sample-json-file)

Canary release is a technique to reduce the risk of introducing a new software version in production by first rolling out the change to a small subset of users. After user validation, the application is rolled out to the larger set of users. Citrix ADC Integrated Canary Deployment Solution stitches together all components of continuous delivery (CD) and makes canary deployment easier for the application developers. This solution uses [Spinnaker](https://www.spinnaker.io/) as the continuous delivery platform and [Kayenta](https://github.com/spinnaker/kayenta) as the Spinnaker plug-in for canary analysis. Kayenta is an open-source canary analysis service that fetches user-configured metrics from their sources, runs statistical tests, and provides an aggregate score for the canary. The score from statistical tests and counters along with the success criteria is used to promote or fail the canary.

Citrix ADC comes with a rich application centric configuration module and provides complete visibility to application traffic and health of application instances. The capabilities of Citrix ADC to generate accurate performance statistics can be leveraged for Canary analysis to take better decisions about the Canary deployment. In this solution, Citrix ADC is integrated with the Spinnaker platform and acts as a source for providing accurate metrics for analyzing Canary deployment using Kayenta. [Citrix ADC Metrics Exporter](https://github.com/citrix/netscaler-metrics-exporter) exports the application performance metrics to the open-source monitoring system Prometheus and you can configure Kayenta to fetch the metrics for canary deployment. Traffic distribution to the canary version can be regulated using the Citrix ADC policy infrastructure. If you want to divert a specific kind of traffic from production to baseline and canary, you can use match expressions to redirect traffic to base line and canary leveraging the rich Citrix ADC policy infrastructure.

For example, if an enterprise wants to direct traffic only from New York and test only the traffic originating from New York then the policy can be based on a location match and only traffic from New York will be diverted to canary and baseline.

The components which are part of the Citrix Integrated Canary Deployment Solution and their functionalities are explained as follows:

-  [GitHub](https://github.com/): GitHub offers all the distributed version control and source code management functionalities provided by Git and additional features.
GitHub has many utilities available for integrating with other tools that form part of your CI/CD pipeline like Docker Hub, Spinnaker and so on.

-  [Docker Hub](https://hub.docker.com/): Docker Hub is a cloud-based repository service provided by Docker for sharing and finding Docker images. You can integrate GitHub with Docker Hub to automatically build images from the source code in GitHub and push the built image to Docker Hub.

-  [Spinnaker](https://www.spinnaker.io/): Spinnaker is an open source, multi-cloud continuous delivery platform for releasing software changes with high velocity and reliance. You can use Spinnaker’s application deployment features to construct and manage continuous delivery workflows. The key deployment management construct in Spinnaker is known as a pipeline. Pipelines in Spinnaker consist of a sequence of actions, known as stages. Spinnaker provides various stages for deploying an application, running a script, performing canary analysis, removing the deployment, and so on. You can integrate Spinnaker with many third party tools to support many extra functionalities.

-  [Prometheus](https://prometheus.io/): Prometheus is an open-source systems monitoring and alerting toolkit. Prometheus is a monitoring system which can maintain huge amount of data in a time series database. Citrix ADC exposes the performance metrics to Spinnaker through Prometheus.

-  [Jenkins](https://jenkins.io/): Jenkins is an open source automation server which helps to automate all sorts of tasks related to building, testing, and delivering or deploying software. Jenkins also supports running custom scripts as part of your deployment cycle.

-  [Citrix ingress controller](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/): Citrix provides an Ingress Controller for Citrix ADC MPX (hardware), Citrix ADC VPX (virtualized), and Citrix ADC CPX (containerized) for bare metal and cloud deployments. The Citrix ingress controller is built around Kubernetes Ingress and automatically configures one or more Citrix ADCs based on the Ingress resource configuration.

## Software Requirements

Following Citrix software versions are required for Citrix Integrated Canary Deployment Solution:

-  Citrix ingress controller build/version: `quay.io/citrix/citrix-k8s-ingress-controller:canary-b1`
-  Citrix ADC CPX version: 13.0-36.2701 and later
-  Exporter version: quay.io/citrix/netscaler-metrics-exporter:1.0.8 and later

## Workflow of a Spinnaker pipeline for Citrix ADC Integrated Canary Deployment Solution

The following diagram explains the workflow of a Spinnaker pipeline for Citrix ADC Integrated Canary Deployment Solution.

![Spinnaker_pipeline](/images/spinnaker_pipeline.png)

The following steps explain the workflow specified in the diagram.

1.  Developers maintain the source code in GitHub, make changes whenever required, and commit the changes to GitHub.
1.  A webhook is configured in GitHub to listen for the source code changes. Whenever the source code is checked in to GitHub, the webhook is triggered and informs Docker Hub to build the image with the new source code. Once the docker image is created, a separate webhook configured in Docker Hub triggers a Spinnaker pipeline.
1.  Once the Spinnaker pipeline is triggered, canary and baseline versions of the image are deployed.
1.  Once the canary and baseline versions are deployed, some percentage of traffic from production is diverted to canary and baseline versions. Citrix ADC collects the performance statistics and exports the statistics to Prometheus. Prometheus feeds these statistics to Kayenta for canary analysis.
1.	Kayenta performs a canary analysis based on the performance statistics and generates a score. Based on the score, the canary deployment is termed as success or failure and the image is rolled out or rolled back.

## Limitations

The following limitations exist for Citrix ADC integrated canary deployment solution:

-  For an existing application which shares Ingress with other applications and requires deploying a canary, either ensure all the applications follow the same deployment strategy or change the Ingress for the application that requires canary deployment.

-  For an Ingress if the domain is same and paths are different, persistence does not work and there is no support for cookie generation with path consideration.

-  For canary deployment, [smart annotations](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/configure/annotations/#smart-annotations) are not taken into account from production to canary and baseline versions. Canary and baseline deployment versions do not inherit the properties of the production version.

-  After the creation of a CRD class, there should be a delay of 10 seconds before creating the CRD object for the class.

## Deploy the Citrix ADC Integrated Canary Deployment Solution in Google cloud Platform

Perform the following steps to deploy the Citrix ADC Integrated Canary Deployment solution in Google Cloud Platform.

1.  Set up the environment and create a GKE cluster using the following commands.

        export GOOGLE_CLOUD_PROJECT=[PROJECT_ID] 
        gcloud config set project $GOOGLE_CLOUD_PROJECT 
        gcloud config set compute/zone us-central1-f
        gcloud services enable container.googleapis.com
        gcloud beta container clusters create kayenta-tutorial 
        --machine-type=n1-standard-2 --enable-stackdriver-kubernetes
1.  Install the plug-in for integrating Prometheus with Stackdriver using the following command.

        kubectl apply --as=admin --as-group=system:masters -f \
        https://storage.googleapis.com/stackdriver-prometheus-documentation/rbac-setup.yml
        curl -sS "https://storage.googleapis.com/stackdriver-prometheus-documentation/prometheus-service.yml" | 
        \sed "s/_stackdriver_project_id:.*/_stackdriver_project_id: $GOOGLE_CLOUD_PROJECT/" | 
        \sed "s/_kubernetes_cluster_name:.*/_kubernetes_cluster_name: kayenta-tutorial/" | 
        \sed "s/_kubernetes_location:.*/_kubernetes_location: us-central1-f/" | 
        \kubectl apply -f -
1.  Deploy Spinnaker in the GKE cluster using the following steps.

    1.  Download the ``quick-install.yml`` file for Spinnaker from [Spinnaker](https://www.spinnaker.io/downloads/kubernetes/quick-install.yml) website.
    2.  Update the ``quick-install.yml`` file to integrate different components starting with Docker Hub. To integrate Spinnaker with Docker Hub, update the values of address, user name, password, email, and repository under ConfigMap in ``quick-install.yml`` file.

                 dockerRegistry:
                    enabled: true
                    accounts:
                     - name: my-docker-registry
                     requiredGroupMembership: []
                     providerVersion: V1
                     permissions: {}
                     address: https://index.docker.io
                     username: <username>
                     password: <password>
                     email: <mail-id>
                     cacheIntervalSeconds: 30
                     clientTimeoutMillis: 60000
                     cacheThreads: 1
                     paginateSize: 100
                     sortTagsByDate: false
                     trackDigests: false
                     insecureRegistry: false
                     repositories:- <repository-name>
                     primaryAccount: my-docker-registry
    1.  Perform the following steps to set up Jenkins.

        >**Note**
        >If Jenkins is installed in one of the nodes of Kubernetes, you must update the firewall rules for that node for public access.

                sudo apt-get update
                sudo apt-get upgrade
                sudo apt-get install openjdk-8-jdk
                wget -q -O 
                - https://jenkins-ci.org/debian/jenkins-ci.org.key |       sudo apt-key add -
                sudo sh -c 'echo deb http://pkg.jenkins-ci.org/debian binary/ > /etc/apt/sources.list.d/jenkins.list'
                sudo apt-get update
                sudo apt-get install jenkins git
                sudo apt-get install software-properties-common python-software-properties apt-transport-https
                sudo add-apt-repository https://dl.bintray.com/spinnaker-releases/debians
    1.  Update the following values in the ``quick-install.yml`` file for integrating Jenkins with Spinnaker.

                data:igor.yml: |
		        enabled: true
		        skipLifeCycleManagement: false
                ci:jenkins:
		        enabled: true
	            masters: 
            - name: master
                  address: <endpoint>
   	            username: <username>
	            password: <password>

    1.  To set up Prometheus and [Grafana](https://grafana.com/), see the Prometheus and Grafana Integration section in Citrix [Citrix ADC metrics exporter](https://github.com/citrix/netscaler-metrics-exporter) and perform the steps.

    1.  To integrate Prometheus with Spinnaker, update the following values in the ``quick-install.yml`` file.

            data:
             config: | 
              deploymentConfigurations:
               canary:
	            enabled: true
        	serviceIntegrations:
                - name: prometheus
	          enabled: true
        	accounts: 
	          - name: my-prometheus
        	endpoint:
                baseUrl: <prometheus-endpoint>
	             supportedTypes:
        	- METRICS_STORE
            data:
             config: |
              deploymentConfigurations:
               metricStores:
                prometheus:
                 enabled: true
                 add_source_metalabels: true
                stackdriver:
	          enabled: true
               period: 30
               enabled: true

    1.  To integrate Slack for notification with Spinnaker, update the following values in the ``quick-install.yml`` file.

            data:
             config: |
              deploymentConfigurations:
               notifications:
                slack:
                 enabled: true
                  botName: <BotName>
                  token: <token>

    1.  To expose Spinnaker securely to public like any other application using Citrix ADC and Citrix ingress controller, see [Citrix ingress controller documentation](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/).
    1.  Verify the progress of the deployment using the following command. Once the deployment is complete, this command outputs all the pods as Ready x/x

            watch kubectl -n spinnaker get pods

    1.  To enable Spinnaker access, forward a local port to the deck component of Spinnaker using the following command:
   
            DECK_POD=$(kubectl -n spinnaker get pods -l \
            cluster=spin-deck,app=spin \
            -o=jsonpath='{.items[0].metadata.name}')
            kubectl -n spinnaker port-forward $DECK_POD 8080:9000 >/dev/null &

    1.  To access Spinnaker, in the Cloud Shell, click the **Web Preview** icon and select **Preview on port 8080**.

## Troubleshooting

For troubleshooting the deployment, perform the following steps.

1.  Go through the ``README`` file and follow the steps.
1.  Check the pod logs for the respective components like Spinnaker, Prometheus, Kayenta, Citrix ADC CPX, exporter, Citrix ingress and so on.
1.  Check the pod logs of the Citrix ingress controller for any configuration related errors while configuring the Citrix proxy.
1.  Search for the ``exception/Exception`` keyword in the Citrix ingress controller pod logs to narrow down the issues.
1.  Check for the logs preceding the search. Check for the configuration that failed and caused the issue.
1.  Check for the reason of failures during configuration.
1.  If the failure happened because of incorrect configuration, correct the configuration.

## Sample JSON file

This topic contains a sample JSON file for a pipeline which deploys a canary version and baseline version of the application.

```JSON
{
  "appConfig": {},
  "description": "This pipeline deploys a canary version of the application, and a baseline (identical to production) version.\nIt compares them, and if the canary is OK, it triggers the production deployment pipeline.",
  "executionEngine": "v2",
  "expectedArtifacts": [
    {
      "defaultArtifact": {
        "kind": "custom"
      },
      "id": "ac842617-988f-48dc-a7a4-7f020d93cc42",
      "matchArtifact": {
        "kind": "docker",
        "name": "index.docker.io/sample/demo",
        "type": "docker/image"
      },
      "useDefaultArtifact": false,
      "usePriorExecution": false
    }
  ],
  "keepWaitingPipelines": false,
  "lastModifiedBy": "anonymous",
  "limitConcurrent": true,
  "parallel": true,
  "parameterConfig": [],
  "stages": [
    {
      "account": "my-kubernetes-account",
      "cloudProvider": "kubernetes",
      "kinds": [
        "Deployment",
        "ConfigMap"
      ],
      "labelSelectors": {
        "selectors": [
          {
            "key": "version",
            "kind": "EQUALS",
            "values": [
              "canary"
            ]
          }
        ]
      },
      "location": "default",
      "name": "Delete Canary",
      "options": {
        "cascading": true
      },
      "refId": "12",
      "requisiteStageRefIds": [
        "19",
        "26"
      ],
      "type": "deleteManifest"
    },
    {
      "account": "my-kubernetes-account",
      "cloudProvider": "kubernetes",
      "kinds": [
        "Deployment"
      ],
      "labelSelectors": {
        "selectors": [
          {
            "key": "version",
            "kind": "EQUALS",
            "values": [
              "baseline"
            ]
          }
        ]
      },
      "location": "default",
      "name": "Delete Baseline",
      "options": {
        "cascading": true
      },
      "refId": "13",
      "requisiteStageRefIds": [
        "19",
        "26"
      ],
      "type": "deleteManifest"
    },
    {
      "name": "Successful deployment",
      "preconditions": [],
      "refId": "14",
      "requisiteStageRefIds": [
        "12",
        "13"
      ],
      "type": "checkPreconditions"
    },
    {
      "application": "sampleapplicaion",
      "expectedArtifacts": [
        {
          "defaultArtifact": {
            "kind": "custom"
          },
          "id": "9185c756-c6cd-49bc-beee-e3f7118f3412",
          "matchArtifact": {
            "kind": "docker",
            "name": "index.docker.io/sample/demo",
            "type": "docker/image"
          },
          "useDefaultArtifact": false,
          "usePriorExecution": false
        }
      ],
      "failPipeline": true,
      "name": "Deploy to Production",
      "pipeline": "7048e5ac-2464-4557-a05a-bec8bdf868fc",
      "refId": "19",
      "requisiteStageRefIds": [
        "25"
      ],
      "stageEnabled": {
        "expression": "\"${ #stage('Canary Analysis')['status'].toString() == 'SUCCEEDED'}\"",
        "type": "expression"
      },
      "type": "pipeline",
      "waitForCompletion": true
    },
    {
      "account": "my-kubernetes-account",
      "cloudProvider": "kubernetes",
      "manifestArtifactAccount": "embedded-artifact",
      "manifests": [
        {
          "apiVersion": "extensions/v1beta1",
          "kind": "Deployment",
          "metadata": {
            "labels": {
              "name": "sampleapplicaion-prod",
              "version": "baseline"
            },
            "name": "sampleapplicaion-baseline-deployment",
            "namespace": "default"
          },
          "spec": {
            "replicas": 4,
            "strategy": {
              "rollingUpdate": {
                "maxSurge": 10,
                "maxUnavailable": 10
              },
              "type": "RollingUpdate"
            },
            "template": {
              "metadata": {
                "labels": {
                  "name": "sampleapplicaion-prod"
                }
              },
              "spec": {
                "containers": [
                  {
                    "image": "index.docker.io/sample/demo:v1",
                    "imagePullPolicy": "Always",
                    "name": "sampleapplicaion-prod",
                    "ports": [
                      {
                        "containerPort": 8080,
                        "name": "port-8080"
                      }
                    ]
                  }
                ]
              }
            }
          }
        }
      ],
      "moniker": {
        "app": "sampleapplicaion"
      },
      "name": "Deploy Baseline",
      "refId": "20",
      "relationships": {
        "loadBalancers": [],
        "securityGroups": []
      },
      "requisiteStageRefIds": [],
      "source": "text",
      "type": "deployManifest"
    },
    {
      "account": "my-kubernetes-account",
      "cloudProvider": "kubernetes",
      "manifestArtifactAccount": "embedded-artifact",
      "manifests": [
        {
          "apiVersion": "extensions/v1beta1",
          "kind": "Deployment",
          "metadata": {
            "labels": {
              "name": "sampleapplicaion-prod",
              "version": "canary"
            },
            "name": "sampleapplicaion-canary-deployment",
            "namespace": "default"
          },
          "spec": {
            "replicas": 4,
            "strategy": {
              "rollingUpdate": {
                "maxSurge": 10,
                "maxUnavailable": 10
              },
              "type": "RollingUpdate"
            },
            "template": {
              "metadata": {
                "labels": {
                  "name": "sampleapplicaion-prod"
                }
              },
              "spec": {
                "containers": [
                  {
                    "image": "index.docker.io/sample/demo",
                    "imagePullPolicy": "Always",
                    "name": "sampleapplicaion-prod",
                    "ports": [
                      {
                        "containerPort": 8080,
                        "name": "port-8080"
                      }
                    ]
                  }
                ]
              }
            }
          }
        }
      ],
      "moniker": {
        "app": "sampleapplicaion"
      },
      "name": "Deploy Canary",
      "refId": "21",
      "relationships": {
        "loadBalancers": [],
        "securityGroups": []
      },
      "requiredArtifactIds": [
        "ac842617-988f-48dc-a7a4-7f020d93cc42"
      ],
      "requisiteStageRefIds": [],
      "source": "text",
      "type": "deployManifest"
    },
    {
      "analysisType": "realTime",
      "canaryConfig": {
        "beginCanaryAnalysisAfterMins": "2",
        "canaryAnalysisIntervalMins": "",
        "canaryConfigId": "7bdb4ab4-f933-4a41-865f-6d3e9c786351",
        "combinedCanaryResultStrategy": "LOWEST",
        "lifetimeDuration": "PT0H5M",
        "metricsAccountName": "my-prometheus",
        "scopes": [
          {
            "controlLocation": "default",
            "controlScope": "k8s-sampleapplicaion.default.80.k8s-sampleapplicaion.default.8080.svc-baseline",
            "experimentLocation": "default",
            "experimentScope": "k8s-sampleapplicaion.default.80.k8s-sampleapplicaion.default.8080.svc-canary",
            "extendedScopeParams": {},
            "scopeName": "default"
          }
        ],
        "scoreThresholds": {
          "marginal": "0",
          "pass": "70"
        },
        "storageAccountName": "kayenta-minio"
      },
      "name": "Canary Analysis",
      "refId": "25",
      "requisiteStageRefIds": [
        "20",
        "21"
      ],
      "type": "kayentaCanary"
    },
    {
      "continuePipeline": false,
      "failPipeline": true,
      "job": "NJob",
      "master": "master",
      "name": "Auto Cleanup:  GCR Image and code revert",
      "parameters": {},
      "refId": "26",
      "requisiteStageRefIds": [
        "25"
      ],
      "stageEnabled": {
        "type": "expression"
      },
      "type": "jenkins"
    }
  ],
  "triggers": [
    {
      "account": "my-docker-registry",
      "enabled": true,
      "expectedArtifactIds": [
        "ac842617-988f-48dc-a7a4-7f020d93cc42"
      ],
      "organization": "sample",
      "payloadConstraints": {},
      "registry": "index.docker.io",
      "repository": "sample/demo",
      "source": "dockerhub",
      "type": "webhook"
    }
  ],
  "updateTs": "1553144362000"
}

A sample json file canary config for spinnaker pipeline

{
  "applications": [
    "sampleapplicaion"
  ],
  "classifier": {
    "groupWeights": {
      "Group 1": 70,
      "Group 2": 30
    },
    "scoreThresholds": {
      "marginal": 75,
      "pass": 95
    }
  },
  "configVersion": "1",
  "createdTimestamp": 1552650414234,
  "createdTimestampIso": "2019-03-15T11:46:54.234Z",
  "description": "Canary Config",
  "judge": {
    "judgeConfigurations": {},
    "name": "NetflixACAJudge-v1.0"
  },
  "metrics": [
    {
      "analysisConfigurations": {
        "canary": {
          "direction": "increase"
        }
      },
      "groups": [
        "Group 1"
      ],
      "name": "Server Response Errors - 5XX",
      "query": {
        "customFilterTemplate": "tot_requests",
        "metricName": "netscaler_lb_vserver_svr_busy_err_rate",
        "serviceType": "prometheus",
        "type": "prometheus"
      },
      "scopeName": "default"
    },
    {
      "analysisConfigurations": {
        "canary": {
          "direction": "either",
          "nanStrategy": "replace"
        }
      },
      "groups": [
        "Group 2"
      ],
      "name": "Server Response Latency - TTFB",
      "query": {
        "customFilterTemplate": "ttfb",
        "metricName": "netscaler_lb_vserver_hits_total",
        "serviceType": "prometheus",
        "type": "prometheus"
      },
      "scopeName": "default"
    }
  ],
  "name": "canary-config",
  "templates": {
    "tot_requests": "lb_vserver_name = \"${scope}\"",
    "ttfb": "lb_vserver_name = \"${scope}\""
  },
  "updatedTimestamp": 1553098513495,
  "updatedTimestampIso": "2019-03-20T16:15:13.495Z"
}
```
