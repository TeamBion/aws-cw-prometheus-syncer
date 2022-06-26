[![Pylint Status](https://app.travis-ci.com/WoodProgrammer/eks-cloudwatch-audit.svg?branch=hot_fix_1)](https://app.travis-ci.com/WoodProgrammer/soprano)

# Cloudwatch Insight Prometheus Exporter

CWInsightExporter allows to produce Prometheus compatible metrics according to the cloudwatch log insights queries.This exporter works as a prometheus exporter belongs to a query fetcher which works as a query broker.

Some of the important metrics like EKS audit, controller-manager .. etc are only produces as a cloudwatch log group by AWS regarding to that we are not able to produce metrics directly with AWS CloudwatchMetrics or exporters.Therefore we developed this tool to fetch and produce Prometheus compatible metrics from cloudwatch logs with cloudwatch Insight queries.

<img height="250" width="1000" src="./img/diagram.png"></img>

<b> Table of contents </b>

- [Getting started](#getting-started)
  - [Deployment](#deploy)
- [Configuration](#configuration)

## Getting Started

* <a href="./deploy/soprano/values.yaml">Quick Start - EKS Audit logs</a>

## Deployment

Helm chart is located in deploy/soprano directory and you can easily setup the helm chart shown at below.

```sh
  $ export BASE_PATH=$(PWD)/deploy/soprano
  
  $ helm upgrade -i aws-cw-prometheus-syncer ${BASE_PATH} -f ${BASE_PATH}/values.yaml
```

### Caveats 
To make this tool able to fetch the results of the CloudwatchInsights queries you should make sure the permissions are setup true.

### Permissions
```json
{
  "Version": "2012-10-17",
  "Statement": [
      {
        "Sid": "LogGroupRetention",
        "Effect": "Allow",
        "Action": [
            "logs:Get*",
            "logs:Describe*",
            "logs:StartQuery",
            "logs:StopQuery",
            "logs:GetQueryResults",
            "cloudwathc:Get*"
        ]
        "Resource": "arn:aws:logs:REGION:ACCOUNT_ID:log-group:LOG-GROUP-NAME"
      }
  ]
}
```

This tools is also able to access AWS API via  IRSA [Recommended way] assumed way so basically you can setup the IRSA like that;

```yaml
serviceAccount:
  create: true
  annotations:
    eks.amazonaws.com/role-arn: ROLE_ARN
```

## Configuration

You can check the helm configuration details overs there ; 

| Parameter                         | Description                                                             | Default                     |
| --------------------------------- | ----------------------------------------------------------------------- | --------------------------- |
| `image.repository`                | Image                                                                   | `emirozbir/soprano
| `eks.region`                | The aws region where you are working                                                                    | `eu-west-1
| `eks.log_group_name`                | Log group address to work on                                                                    | `/aws/eks/test-cluster/cluster
| `servicemonitor.exporter_key`                |  Release name of the kube-prometheus stack                                                                     | `eu-west-1
| `servicemonitor.namespace`                | Prometheus operator namespace on                                                                   | `eu-west-1
| `exporter.port`                | Exposed port value on                                                                   | `9877
| `serviceAccount.annotations`                | Annocations for the IRSA usage or generic purpose staff on                                                                   | `eks.amazonaws.com/role-arn: arn:aws:iam::ACCOUNT_ID:role/ROLE-FOR-SOPRANO"

<b>Important:</b>

To show respect to the James Gandolfini I keep the helm chart name as Soprano.