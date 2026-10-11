using './workload.bicep'

param demoApiKey = readEnvironmentVariable('DEMO_API_KEY')
param registryName = 'REPLACE_WITH_FOUNDATION_REGISTRY_NAME'
param workloadIdentityName = 'id-sre-mvp'
param applicationInsightsName = 'appi-sre-mvp'
param containerAppsEnvironmentName = 'cae-sre-mvp'
param actionGroupName = 'ag-sre-mvp'
param environmentName = 'mvp'
param imageNameAndTag = 'sre-showcase:latest'
param isFaultInjectionEnabled = false
param minimumReplicas = 0
param shouldEnableMonitoring = true
param minimumAlertRequestCount = 20
param monitoredApplicationSlugs = [
  'retail-checkout'
  'order-fulfillment'
  'payments-api'
  'banking-ledger'
]
param tags = {
  application: 'sre-agent-enterprise-showcase'
  costCenter: 'REPLACE_WITH_COST_CENTER'
  environment: 'mvp'
  expiresOn: '2026-10-31'
  managedBy: 'bicep'
  owner: 'REPLACE_WITH_OWNER'
}
