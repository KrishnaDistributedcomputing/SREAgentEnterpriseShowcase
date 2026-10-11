targetScope = 'resourceGroup'

metadata name = 'SRE Agent Showcase MVP Platform'
metadata description = 'Deploys shared identity, registry, observability, and Container Apps platform resources.'

@description('Email address that receives Azure Monitor action group notifications. No action group is created when omitted.')
param alertEmail string?

@description('Short environment name used in resource names.')
@minLength(2)
@maxLength(12)
param environmentName string

@description('Azure region for the platform resources.')
param location string

@description('Log Analytics retention period in days.')
@minValue(30)
param logRetentionDays int

@description('Short prefix used in resource names.')
@minLength(2)
@maxLength(12)
param resourcePrefix string

@description('Azure resource tags applied to every supported resource.')
param tags object

var acrPullRoleDefinitionId = subscriptionResourceId(
  'Microsoft.Authorization/roleDefinitions',
  '7f951dda-4ed3-4680-a7ca-43fe172d538d'
)
var actionGroupName = 'ag-${resourcePrefix}-${environmentName}'
var applicationInsightsName = 'appi-${resourcePrefix}-${environmentName}'
var containerAppsEnvironmentName = 'cae-${resourcePrefix}-${environmentName}'
var logAnalyticsName = 'log-${resourcePrefix}-${environmentName}'
var registryName = take(
  toLower(replace('${resourcePrefix}${environmentName}${uniqueString(resourceGroup().id)}', '-', '')),
  50
)
var workloadIdentityName = 'id-${resourcePrefix}-${environmentName}'

resource registry 'Microsoft.ContainerRegistry/registries@2023-11-01-preview' = {
  name: registryName
  location: location
  tags: tags
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: false
    anonymousPullEnabled: false
    dataEndpointEnabled: false
    publicNetworkAccess: 'Enabled'
    zoneRedundancy: 'Disabled'
    policies: {
      exportPolicy: {
        status: 'disabled'
      }
      quarantinePolicy: {
        status: 'disabled'
      }
      retentionPolicy: {
        days: 7
        status: 'disabled'
      }
      trustPolicy: {
        status: 'disabled'
        type: 'Notary'
      }
    }
  }
}

resource workloadIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: workloadIdentityName
  location: location
  tags: tags
}

resource registryPullAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(registry.id, workloadIdentity.id, acrPullRoleDefinitionId)
  scope: registry
  properties: {
    principalId: workloadIdentity.properties.principalId
    principalType: 'ServicePrincipal'
    roleDefinitionId: acrPullRoleDefinitionId
  }
}

resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: logAnalyticsName
  location: location
  tags: tags
  properties: {
    features: {
      enableLogAccessUsingOnlyResourcePermissions: true
    }
    publicNetworkAccessForIngestion: 'Enabled'
    publicNetworkAccessForQuery: 'Enabled'
    retentionInDays: logRetentionDays
    sku: {
      name: 'PerGB2018'
    }
  }
}

resource applicationInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: applicationInsightsName
  location: location
  tags: tags
  kind: 'web'
  properties: {
    Application_Type: 'web'
    DisableIpMasking: false
    DisableLocalAuth: false
    ForceCustomerStorageForProfiler: false
    IngestionMode: 'LogAnalytics'
    RetentionInDays: logRetentionDays
    SamplingPercentage: 100
    WorkspaceResourceId: logAnalytics.id
    publicNetworkAccessForIngestion: 'Enabled'
    publicNetworkAccessForQuery: 'Enabled'
  }
}

resource containerAppsEnvironment 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: containerAppsEnvironmentName
  location: location
  tags: tags
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

resource actionGroup 'Microsoft.Insights/actionGroups@2023-01-01' = if (!empty(alertEmail)) {
  name: actionGroupName
  location: 'global'
  tags: tags
  properties: {
    armRoleReceivers: []
    automationRunbookReceivers: []
    azureAppPushReceivers: []
    azureFunctionReceivers: []
    emailReceivers: [
      {
        emailAddress: alertEmail!
        name: 'MvpOwner'
        useCommonAlertSchema: true
      }
    ]
    enabled: true
    eventHubReceivers: []
    groupShortName: take('${resourcePrefix}${environmentName}', 12)
    itsmReceivers: []
    logicAppReceivers: []
    smsReceivers: []
    voiceReceivers: []
    webhookReceivers: []
  }
}

@description('Resource ID of the optional Azure Monitor action group.')
output actionGroupResourceId string? = !empty(alertEmail) ? actionGroup.id : null

@description('Resource name of the optional Azure Monitor action group.')
output actionGroupResourceName string? = !empty(alertEmail) ? actionGroup.name : null

@description('Application ID used to configure the Azure SRE Agent Application Insights connector.')
output applicationInsightsAppId string = applicationInsights.properties.AppId

@description('Application Insights resource ID.')
output applicationInsightsResourceId string = applicationInsights.id

@description('Application Insights resource name.')
output applicationInsightsResourceName string = applicationInsights.name

@description('Container Apps environment resource ID.')
output containerAppsEnvironmentResourceId string = containerAppsEnvironment.id

@description('Container Apps environment resource name.')
output containerAppsEnvironmentResourceName string = containerAppsEnvironment.name

@description('Log Analytics workspace resource ID.')
output logAnalyticsResourceId string = logAnalytics.id

@description('Log Analytics workspace resource name.')
output logAnalyticsResourceName string = logAnalytics.name

@description('Azure Container Registry login server.')
output registryLoginServer string = registry.properties.loginServer

@description('Azure Container Registry resource name.')
output registryName string = registry.name

@description('Workload managed identity client ID.')
output workloadIdentityClientId string = workloadIdentity.properties.clientId

@description('Workload managed identity resource ID.')
output workloadIdentityResourceId string = workloadIdentity.id

@description('Workload managed identity resource name.')
output workloadIdentityResourceName string = workloadIdentity.name
