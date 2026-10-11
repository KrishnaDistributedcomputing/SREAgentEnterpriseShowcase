using './foundation.bicep'

param resourceGroupName = 'rg-sre-showcase-mvp'
param location = 'westus2'
param resourcePrefix = 'sre'
param environmentName = 'mvp'
param budgetAmount = 85
param budgetStartDate = '2026-10-01'
param budgetContactEmails = [
  'REPLACE_WITH_OWNER_EMAIL'
]
param alertEmail = 'REPLACE_WITH_OWNER_EMAIL'
param logRetentionDays = 30
param tags = {
  application: 'sre-agent-enterprise-showcase'
  costCenter: 'REPLACE_WITH_COST_CENTER'
  environment: 'mvp'
  expiresOn: '2026-10-31'
  managedBy: 'bicep'
  owner: 'REPLACE_WITH_OWNER'
}
