using './main.bicep'

param environmentName = 'demo'
param containerImage = 'REPLACE_WITH_REGISTRY.azurecr.io/sre-showcase:latest'
param registryServer = 'REPLACE_WITH_REGISTRY.azurecr.io'
param workloadIdentityResourceId = '/subscriptions/REPLACE/resourceGroups/REPLACE/providers/Microsoft.ManagedIdentity/userAssignedIdentities/REPLACE'
param workloadIdentityClientId = 'REPLACE_WITH_CLIENT_ID'
param enableFaultInjection = false

