# Contoso Production Architecture Diagram Summary

## Containers

- VNet: `vnet-contoso-auea-001` (10.10.0.0/16)
  - Subnet: `snet-frontend` (10.10.1.0/24)
  - Subnet: `snet-backend` (10.10.2.0/24)
  - Subnet: `snet-data` (10.10.3.0/24)
  - Firewall & Routing cluster
- Monitoring cluster

## Resources

### Frontend Subnet
- `NSG-Frontend` (Network Security Group)
- `agw-contoso` (Application Gateway WAF)
- `asp-contoso-prod` (App Service Plan)
- `app-frontend-portal` (Web App)

### Backend Subnet
- `NSG-Backend` (Network Security Group)
- `asp-contoso-backend` (App Service Plan)
- `app-order-api` (Backend App Service)
- `func-order-processor` (Function App)
- `sb-contoso-orders` (Service Bus)

### Data Subnet
- `NSG-Data` (Network Security Group)
- `sqlsrv-contoso` (SQL Server)
- `sqldb-orders` (SQL Database)
- `stcontosodata001` (Storage Account)
- `kv-contoso-prod` (Key Vault)
- `pe-sql` (SQL Private Endpoint)
- `pe-storage` (Storage Private Endpoint)
- `pe-keyvault` (Key Vault Private Endpoint)

### Firewall & Routing
- `azfw-contoso` (Azure Firewall)
- `Route Table` (default route to Firewall)

### Monitoring
- `law-contoso-prod` (Log Analytics Workspace)
- `appi-contoso` (Application Insights)

## Connections

- `Users` → `afd-contoso` (Azure Front Door)
- `afd-contoso` → `agw-contoso` (Application Gateway)
- `agw-contoso` → `app-frontend-portal` (Web App)
- `app-frontend-portal` → `app-order-api` (Backend API)
- `app-order-api` → `sqldb-orders` (SQL Database via private connection)
- `app-order-api` → `stcontosodata001` (Storage via private connection)
- `func-order-processor` → `sb-contoso-orders` (Service Bus)
- `sb-contoso-orders` → `func-order-processor` (message processing)
- `func-order-processor` → `sqldb-orders` (SQL Database via private connection)
- `app-frontend-portal` → `kv-contoso-prod` (Key Vault secrets)
- `app-order-api` → `kv-contoso-prod` (Key Vault secrets)
- `func-order-processor` → `kv-contoso-prod` (Key Vault secrets)
- `sqlsrv-contoso` → `sqldb-orders` (hosts SQL database)
- `app-frontend-portal` → `azfw-contoso` (outbound traffic)
- `app-order-api` → `azfw-contoso` (outbound traffic)
- `func-order-processor` → `azfw-contoso` (outbound traffic)
- `sqldb-orders` → `law-contoso-prod` (logs)
- `stcontosodata001` → `law-contoso-prod` (logs)
- `app-frontend-portal` → `law-contoso-prod` (logs)
- `app-order-api` → `law-contoso-prod` (logs)
- `func-order-processor` → `law-contoso-prod` (logs)
- `app-frontend-portal` → `appi-contoso` (telemetry)
- `app-order-api` → `appi-contoso` (telemetry)
- `func-order-processor` → `appi-contoso` (telemetry)

## Layout Notes

- Top: `Users` + `afd-contoso`
- Below Front Door: `agw-contoso`
- Middle: `app-frontend-portal` and `app-order-api`
- Right: `func-order-processor` and `sb-contoso-orders`
- Bottom: Data tier (`sqlsrv-contoso`, `sqldb-orders`, `stcontosodata001`, `kv-contoso-prod`)
- Bottom left: `azfw-contoso`
- Bottom center: monitoring resources (`law-contoso-prod`, `appi-contoso`)
- All internal resources placed inside the single VNet container with subnet boundaries.
