targetScope = 'resourceGroup'

metadata name = 'SRE Agent Showcase MVP Workload'
metadata description = 'Deploys the 15 application fleet with MVP alerts and availability tests.'

@description('Name of the existing Azure Monitor action group. Alert actions are omitted when not supplied.')
param actionGroupName string?

@description('Name of the existing workspace-based Application Insights resource.')
param applicationInsightsName string

@description('Name of the existing Container Apps environment.')
param containerAppsEnvironmentName string

@secure()
@description('Fault-control key stored as a Container Apps secret.')
param demoApiKey string

@description('Short environment name used in resource names and telemetry.')
@minLength(2)
@maxLength(12)
param environmentName string = 'mvp'

@description('Enable bounded fault injection in the non-production showcase.')
param isFaultInjectionEnabled bool = false

@description('Container image name and tag in the existing registry.')
param imageNameAndTag string = 'sre-showcase:latest'

@description('Azure region for application, alert, and availability resources.')
param location string = resourceGroup().location

@allowed([
  0
  1
])
@description('Minimum replicas per application. Use one only during scheduled demonstrations.')
param minimumReplicas int = 0

@description('Application slugs that receive MVP latency, error, and availability monitoring.')
param monitoredApplicationSlugs array = [
  'retail-checkout'
  'order-fulfillment'
  'payments-api'
  'banking-ledger'
]

@description('Minimum request count required before a latency or error-rate alert can fire.')
@minValue(1)
param minimumAlertRequestCount int = 20

@description('Name of the existing Azure Container Registry.')
param registryName string

@description('Enable Azure Monitor alert rules and availability tests.')
param shouldEnableMonitoring bool = true

@description('Azure resource tags applied to every supported resource.')
param tags object = {
  application: 'sre-agent-enterprise-showcase'
  environment: environmentName
  managedBy: 'bicep'
}

@description('Name of the existing workload user-assigned managed identity.')
param workloadIdentityName string

var actionGroupActions = empty(actionGroupName)
  ? []
  : [
      {
        actionGroupId: resourceId('Microsoft.Insights/actionGroups', actionGroupName!)
      }
    ]
var actionGroupIds = empty(actionGroupName)
  ? []
  : [
      resourceId('Microsoft.Insights/actionGroups', actionGroupName!)
    ]
var applicationConfigurations = [
  {
    latencyObjectiveMs: 450
    slug: 'retail-checkout'
  }
  {
    latencyObjectiveMs: 300
    slug: 'payments-api'
  }
  {
    latencyObjectiveMs: 500
    slug: 'inventory-service'
  }
  {
    latencyObjectiveMs: 800
    slug: 'order-fulfillment'
  }
  {
    latencyObjectiveMs: 250
    slug: 'banking-ledger'
  }
  {
    latencyObjectiveMs: 1000
    slug: 'claims-processing'
  }
  {
    latencyObjectiveMs: 600
    slug: 'patient-scheduling'
  }
  {
    latencyObjectiveMs: 700
    slug: 'airline-reservation'
  }
  {
    latencyObjectiveMs: 900
    slug: 'logistics-tracking'
  }
  {
    latencyObjectiveMs: 350
    slug: 'media-streaming'
  }
  {
    latencyObjectiveMs: 200
    slug: 'identity-access'
  }
  {
    latencyObjectiveMs: 400
    slug: 'iot-ingestion'
  }
  {
    latencyObjectiveMs: 1500
    slug: 'data-pipeline'
  }
  {
    latencyObjectiveMs: 300
    slug: 'collaboration-api'
  }
  {
    latencyObjectiveMs: 1200
    slug: 'ai-inference-gateway'
  }
]

resource registry 'Microsoft.ContainerRegistry/registries@2023-11-01-preview' existing = {
  name: registryName
}

resource workloadIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' existing = {
  name: workloadIdentityName
}

resource applicationInsights 'Microsoft.Insights/components@2020-02-02' existing = {
  name: applicationInsightsName
}

resource containerAppsEnvironment 'Microsoft.App/managedEnvironments@2024-03-01' existing = {
  name: containerAppsEnvironmentName
}

resource applications 'Microsoft.App/containerApps@2024-03-01' = [
  for application in applicationConfigurations: {
    name: 'ca-${application.slug}-${environmentName}'
    location: location
    tags: union(tags, {
      service: application.slug
    })
    identity: {
      type: 'UserAssigned'
      userAssignedIdentities: {
        '${workloadIdentity.id}': {}
      }
    }
    properties: {
      managedEnvironmentId: containerAppsEnvironment.id
      configuration: {
        activeRevisionsMode: 'Single'
        ingress: {
          allowInsecure: false
          external: true
          targetPort: 8080
          transport: 'auto'
        }
        registries: [
          {
            identity: workloadIdentity.id
            server: registry.properties.loginServer
          }
        ]
        secrets: [
          {
            name: 'demo-api-key'
            value: demoApiKey
          }
        ]
      }
      template: {
        containers: [
          {
            name: application.slug
            image: '${registry.properties.loginServer}/${imageNameAndTag}'
            env: [
              {
                name: 'APP_SLUG'
                value: application.slug
              }
              {
                name: 'DEPLOYMENT_ENVIRONMENT'
                value: environmentName
              }
              {
                name: 'SHOWCASE_ROOT'
                value: '/workspace'
              }
              {
                name: 'ENABLE_FAULT_INJECTION'
                value: string(isFaultInjectionEnabled)
              }
              {
                name: 'DEMO_API_KEY'
                secretRef: 'demo-api-key'
              }
              {
                name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
                value: applicationInsights.properties.ConnectionString
              }
              {
                name: 'AZURE_CLIENT_ID'
                value: workloadIdentity.properties.clientId
              }
            ]
            probes: [
              {
                type: 'Liveness'
                httpGet: {
                  path: '/health/live'
                  port: 8080
                  scheme: 'HTTP'
                }
                initialDelaySeconds: 10
                periodSeconds: 30
              }
              {
                type: 'Readiness'
                httpGet: {
                  path: '/health/ready'
                  port: 8080
                  scheme: 'HTTP'
                }
                initialDelaySeconds: 5
                periodSeconds: 10
              }
            ]
            resources: {
              cpu: json('0.25')
              memory: '0.5Gi'
            }
          }
        ]
        scale: {
          maxReplicas: 2
          minReplicas: minimumReplicas
          rules: [
            {
              name: 'http'
              http: {
                metadata: {
                  concurrentRequests: '20'
                }
              }
            }
          ]
        }
      }
    }
  }
]

resource availabilityTests 'Microsoft.Insights/webTests@2022-06-15' = [
  for (application, index) in applicationConfigurations: if (shouldEnableMonitoring && contains(monitoredApplicationSlugs, application.slug)) {
    name: 'web-${application.slug}-${environmentName}'
    location: location
    tags: union(tags, {
      'hidden-link:${applicationInsights.id}': 'Resource'
      service: application.slug
    })
    kind: 'standard'
    properties: {
      Description: 'External readiness check for ${application.slug}.'
      Enabled: true
      Frequency: 300
      Kind: 'standard'
      Locations: [
        {
          Id: 'us-tx-sn1-azr'
        }
        {
          Id: 'us-fl-mia-edge'
        }
      ]
      Name: '${application.slug} readiness'
      Request: {
        FollowRedirects: false
        HttpVerb: 'GET'
        ParseDependentRequests: false
        RequestUrl: 'https://${applications[index].properties.configuration.ingress.fqdn}/health/ready'
      }
      RetryEnabled: true
      SyntheticMonitorId: 'web-${application.slug}-${environmentName}'
      Timeout: 30
      ValidationRules: {
        ExpectedHttpStatusCode: 200
        SSLCheck: true
        SSLCertRemainingLifetimeCheck: 7
      }
    }
  }
]

resource availabilityAlerts 'Microsoft.Insights/metricAlerts@2018-03-01' = [
  for application in applicationConfigurations: if (shouldEnableMonitoring && contains(monitoredApplicationSlugs, application.slug)) {
    name: 'alert-${application.slug}-availability-${environmentName}'
    location: 'global'
    tags: union(tags, {
      'hidden-link:${applicationInsights.id}': 'Resource'
      'hidden-link:${resourceId('Microsoft.Insights/webtests', 'web-${application.slug}-${environmentName}')}': 'Resource'
      service: application.slug
    })
    properties: {
      actions: actionGroupActions
      autoMitigate: true
      criteria: {
        'odata.type': 'Microsoft.Azure.Monitor.WebtestLocationAvailabilityCriteria'
        componentId: applicationInsights.id
        failedLocationCount: 2
        webTestId: resourceId('Microsoft.Insights/webtests', 'web-${application.slug}-${environmentName}')
      }
      description: 'Readiness availability failed from both MVP test locations for ${application.slug}.'
      enabled: true
      evaluationFrequency: 'PT5M'
      scopes: [
        resourceId('Microsoft.Insights/webtests', 'web-${application.slug}-${environmentName}')
        applicationInsights.id
      ]
      severity: 1
      windowSize: 'PT5M'
    }
    dependsOn: [
      availabilityTests
    ]
  }
]

resource latencyAlerts 'Microsoft.Insights/scheduledQueryRules@2023-12-01' = [
  for application in applicationConfigurations: if (shouldEnableMonitoring && contains(monitoredApplicationSlugs, application.slug)) {
    name: 'alert-${application.slug}-latency-${environmentName}'
    location: location
    tags: union(tags, {
      service: application.slug
    })
    kind: 'LogAlert'
    properties: {
      actions: {
        actionGroups: actionGroupIds
      }
      autoMitigate: true
      checkWorkspaceAlertsStorageConfigured: false
      criteria: {
        allOf: [
          {
            dimensions: []
            failingPeriods: {
              minFailingPeriodsToAlert: 1
              numberOfEvaluationPeriods: 1
            }
            operator: 'GreaterThan'
            query: 'AppRequests | where AppRoleName == "${application.slug}" | summarize RequestCount=count(), P95=percentile(DurationMs, 95) | where RequestCount >= ${minimumAlertRequestCount} and P95 > ${application.latencyObjectiveMs}'
            threshold: 0
            timeAggregation: 'Count'
          }
        ]
      }
      description: 'SRE-SHOWCASE ${application.slug} p95 latency exceeded ${application.latencyObjectiveMs} ms.'
      displayName: 'SRE-SHOWCASE ${application.slug} latency'
      enabled: true
      evaluationFrequency: 'PT5M'
      muteActionsDuration: 'PT15M'
      scopes: [
        applicationInsights.id
      ]
      severity: 2
      skipQueryValidation: false
      windowSize: 'PT5M'
    }
  }
]

resource errorRateAlerts 'Microsoft.Insights/scheduledQueryRules@2023-12-01' = [
  for application in applicationConfigurations: if (shouldEnableMonitoring && contains(monitoredApplicationSlugs, application.slug)) {
    name: 'alert-${application.slug}-errors-${environmentName}'
    location: location
    tags: union(tags, {
      service: application.slug
    })
    kind: 'LogAlert'
    properties: {
      actions: {
        actionGroups: actionGroupIds
      }
      autoMitigate: true
      checkWorkspaceAlertsStorageConfigured: false
      criteria: {
        allOf: [
          {
            dimensions: []
            failingPeriods: {
              minFailingPeriodsToAlert: 1
              numberOfEvaluationPeriods: 1
            }
            operator: 'GreaterThan'
            query: 'AppRequests | where AppRoleName == "${application.slug}" | summarize RequestCount=count(), FailedRequests=countif(Success == false) | extend ErrorRate=100.0 * FailedRequests / RequestCount | where RequestCount >= ${minimumAlertRequestCount} and ErrorRate > 5.0'
            threshold: 0
            timeAggregation: 'Count'
          }
        ]
      }
      description: 'SRE-SHOWCASE ${application.slug} server error rate exceeded five percent.'
      displayName: 'SRE-SHOWCASE ${application.slug} errors'
      enabled: true
      evaluationFrequency: 'PT5M'
      muteActionsDuration: 'PT15M'
      scopes: [
        applicationInsights.id
      ]
      severity: 1
      skipQueryValidation: false
      windowSize: 'PT5M'
    }
  }
]

@description('Application Insights resource ID used by the Azure SRE Agent connector.')
output applicationInsightsResourceId string = applicationInsights.id

@description('Application URLs for all 15 scenarios.')
output applicationUrls array = [
  for (application, index) in applicationConfigurations: {
    name: application.slug
    url: 'https://${applications[index].properties.configuration.ingress.fqdn}'
  }
]

@description('Application slugs with alerts and availability tests enabled.')
output monitoredApplications array = monitoredApplicationSlugs
