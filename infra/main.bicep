targetScope = 'resourceGroup'

@description('Azure region for all showcase resources.')
param location string = resourceGroup().location

@description('Short environment name used in resource names.')
@minLength(2)
@maxLength(12)
param environmentName string = 'demo'

@description('Container image shared by all scenarios.')
param containerImage string

@description('Container registry server, such as contoso.azurecr.io.')
param registryServer string

@description('Resource ID of a user-assigned identity with AcrPull access.')
param workloadIdentityResourceId string

@description('Client ID of the user-assigned workload identity.')
param workloadIdentityClientId string

@secure()
@description('Fault-control key stored as a Container Apps secret.')
param demoApiKey string

@description('Enable fault injection in the non-production showcase.')
param enableFaultInjection bool = false

@allowed([
  0
  1
])
@description('Minimum replicas per application. Use 1 during live demos to avoid cold starts.')
param minimumReplicas int = 0

var applicationSlugs = [
  'retail-checkout'
  'payments-api'
  'inventory-service'
  'order-fulfillment'
  'banking-ledger'
  'claims-processing'
  'patient-scheduling'
  'airline-reservation'
  'logistics-tracking'
  'media-streaming'
  'identity-access'
  'iot-ingestion'
  'data-pipeline'
  'collaboration-api'
  'ai-inference-gateway'
]

resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: 'log-sre-${environmentName}'
  location: location
  properties: {
    retentionInDays: 30
    sku: {
      name: 'PerGB2018'
    }
  }
}

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: 'appi-sre-${environmentName}'
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
  }
}

resource environment 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: 'cae-sre-${environmentName}'
  location: location
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalytics.properties.customerId
        sharedKey: logAnalytics.listKeys().primarySharedKey
      }
    }
  }
}

resource applications 'Microsoft.App/containerApps@2024-03-01' = [
  for slug in applicationSlugs: {
    name: 'ca-${slug}-${environmentName}'
    location: location
    identity: {
      type: 'UserAssigned'
      userAssignedIdentities: {
        '${workloadIdentityResourceId}': {}
      }
    }
    properties: {
      managedEnvironmentId: environment.id
      configuration: {
        activeRevisionsMode: 'Single'
        ingress: {
          external: true
          targetPort: 8080
          transport: 'auto'
          allowInsecure: false
        }
        registries: [
          {
            server: registryServer
            identity: workloadIdentityResourceId
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
            name: slug
            image: containerImage
            env: [
              {
                name: 'APP_SLUG'
                value: slug
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
                value: string(enableFaultInjection)
              }
              {
                name: 'DEMO_API_KEY'
                secretRef: 'demo-api-key'
              }
              {
                name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
                value: appInsights.properties.ConnectionString
              }
              {
                name: 'AZURE_CLIENT_ID'
                value: workloadIdentityClientId
              }
            ]
            resources: {
              cpu: json('0.25')
              memory: '0.5Gi'
            }
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
          }
        ]
        scale: {
          minReplicas: minimumReplicas
          maxReplicas: 2
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

output applicationInsightsResourceId string = appInsights.id
output logAnalyticsResourceId string = logAnalytics.id
output applicationUrls array = [
  for (slug, index) in applicationSlugs: {
    slug: slug
    url: 'https://${applications[index].properties.configuration.ingress.fqdn}'
  }
]
