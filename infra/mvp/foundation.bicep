targetScope = 'subscription'

metadata name = 'SRE Agent Showcase MVP Foundation'
metadata description = 'Creates the resource group, cost budget, and shared Azure platform resources.'

@description('Email address that receives Azure Monitor notifications. No action group is created when omitted.')
param alertEmail string?

@description('Monthly MVP budget amount in the subscription billing currency.')
@minValue(1)
param budgetAmount int = 85

@description('First day of the budget period in YYYY-MM-DD format.')
param budgetStartDate string

@description('Email addresses that receive cost budget notifications. No budget is created when empty.')
param budgetContactEmails array = []

@description('Short environment name used in resource names.')
@minLength(2)
@maxLength(12)
param environmentName string = 'mvp'

@description('Azure region for the resource group and platform resources.')
param location string = deployment().location

@description('Log Analytics retention period in days.')
@minValue(30)
param logRetentionDays int = 30

@description('Name of the resource group that contains the showcase.')
param resourceGroupName string

@description('Short prefix used in resource names.')
@minLength(2)
@maxLength(12)
param resourcePrefix string = 'sre'

@description('Create a resource-group-scoped monthly cost budget when contact emails are supplied.')
param shouldCreateBudget bool = true

@description('Azure resource tags applied to every supported resource.')
param tags object = {
  application: 'sre-agent-enterprise-showcase'
  environment: environmentName
  managedBy: 'bicep'
}

resource showcaseResourceGroup 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: resourceGroupName
  location: location
  tags: tags
}

resource budget 'Microsoft.Consumption/budgets@2023-05-01' = if (shouldCreateBudget && !empty(budgetContactEmails)) {
  name: 'budget-${resourcePrefix}-${environmentName}'
  properties: {
    amount: budgetAmount
    category: 'Cost'
    filter: {
      dimensions: {
        name: 'ResourceGroupName'
        operator: 'In'
        values: [
          resourceGroupName
        ]
      }
    }
    notifications: {
      Actual_50_Percent: {
        contactEmails: budgetContactEmails
        contactGroups: []
        contactRoles: []
        enabled: true
        operator: 'GreaterThanOrEqualTo'
        threshold: 50
        thresholdType: 'Actual'
      }
      Actual_75_Percent: {
        contactEmails: budgetContactEmails
        contactGroups: []
        contactRoles: []
        enabled: true
        operator: 'GreaterThanOrEqualTo'
        threshold: 75
        thresholdType: 'Actual'
      }
      Forecast_90_Percent: {
        contactEmails: budgetContactEmails
        contactGroups: []
        contactRoles: []
        enabled: true
        operator: 'GreaterThanOrEqualTo'
        threshold: 90
        thresholdType: 'Forecasted'
      }
      Actual_100_Percent: {
        contactEmails: budgetContactEmails
        contactGroups: []
        contactRoles: []
        enabled: true
        operator: 'GreaterThanOrEqualTo'
        threshold: 100
        thresholdType: 'Actual'
      }
    }
    timeGrain: 'Monthly'
    timePeriod: {
      startDate: budgetStartDate
    }
  }
}

module platform './modules/platform.bicep' = {
  name: 'platform-${environmentName}'
  scope: showcaseResourceGroup
  params: {
    alertEmail: alertEmail
    environmentName: environmentName
    location: location
    logRetentionDays: logRetentionDays
    resourcePrefix: resourcePrefix
    tags: tags
  }
}

@description('Resource ID of the optional Azure Monitor action group.')
output actionGroupResourceId string? = platform.outputs.actionGroupResourceId

@description('Resource name of the optional Azure Monitor action group.')
output actionGroupResourceName string? = platform.outputs.actionGroupResourceName

@description('Application ID used by the Azure SRE Agent Application Insights connector.')
output applicationInsightsAppId string = platform.outputs.applicationInsightsAppId

@description('Application Insights resource ID.')
output applicationInsightsResourceId string = platform.outputs.applicationInsightsResourceId

@description('Application Insights resource name.')
output applicationInsightsResourceName string = platform.outputs.applicationInsightsResourceName

@description('Container Apps environment resource name.')
output containerAppsEnvironmentResourceName string = platform.outputs.containerAppsEnvironmentResourceName

@description('Log Analytics workspace resource ID.')
output logAnalyticsResourceId string = platform.outputs.logAnalyticsResourceId

@description('Log Analytics workspace resource name.')
output logAnalyticsResourceName string = platform.outputs.logAnalyticsResourceName

@description('Azure Container Registry login server used by the image build.')
output registryLoginServer string = platform.outputs.registryLoginServer

@description('Azure Container Registry resource name used by the image build.')
output registryName string = platform.outputs.registryName

@description('Showcase resource group name.')
output resourceGroupName string = showcaseResourceGroup.name

@description('Workload managed identity client ID.')
output workloadIdentityClientId string = platform.outputs.workloadIdentityClientId

@description('Workload managed identity resource name.')
output workloadIdentityResourceName string = platform.outputs.workloadIdentityResourceName
