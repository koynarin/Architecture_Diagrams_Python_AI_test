"""
Azure Architecture Diagram Generator for Contoso Production Environment
Generates PNG, DOT, and Draw.io diagrams for the requested VNet/subnet architecture.
"""

import subprocess
from diagrams import Diagram, Cluster, Edge, Node
from diagrams.azure.compute import AppServices, FunctionApps
from diagrams.azure.network import (
    ApplicationGateway,
    FrontDoors,
    NetworkSecurityGroupsClassic,
    Firewall,
    RouteTables
)
from diagrams.azure.database import SQLServers, SQLDatabases
from diagrams.azure.storage import StorageAccounts
from diagrams.azure.security import KeyVaults
from diagrams.azure.integration import ServiceBus
from diagrams.azure.analytics import LogAnalyticsWorkspaces
from diagrams.azure.devops import ApplicationInsights
from diagrams.onprem.client import Users

# Graph attributes for a clear, orthogonal layout
graph_attr = {
    "splines": "ortho",
    "nodesep": "0.8",
    "ranksep": "1.2",
    "fontsize": "14",
    "bgcolor": "white",
    "pad": "0.5",
    "compound": "true"
}

# Cluster attributes for each tier or group
vnet_cluster_attr = {
    "fontsize": "14",
    "bgcolor": "#E8F4F8",
    "style": "dashed",
    "margin": "25"
}

frontend_cluster_attr = {
    "fontsize": "13",
    "bgcolor": "#E3F2FD",
    "style": "rounded",
    "margin": "15"
}

app_cluster_attr = {
    "fontsize": "13",
    "bgcolor": "#F3E5F5",
    "style": "rounded",
    "margin": "15"
}

data_cluster_attr = {
    "fontsize": "13",
    "bgcolor": "#FFF3E0",
    "style": "rounded",
    "margin": "15"
}

firewall_cluster_attr = {
    "fontsize": "13",
    "bgcolor": "#FFEBEE",
    "style": "rounded",
    "margin": "15"
}

monitoring_cluster_attr = {
    "fontsize": "13",
    "bgcolor": "#E8F5E9",
    "style": "rounded",
    "margin": "15"
}

with Diagram(
    "Contoso Production Architecture",
    filename="diagrams/contoso_architecture",
    outformat=["png", "dot"],
    show=False,
    direction="TB",
    graph_attr=graph_attr
):
    # External access
    users = Users("Users")
    afd = FrontDoors("afd-contoso\n(Azure Front Door)")

    with Cluster("vnet-contoso-auea-001\n(10.10.0.0/16)", graph_attr=vnet_cluster_attr):
        with Cluster("snet-frontend\n(10.10.1.0/24)", graph_attr=frontend_cluster_attr):
            nsg_frontend = NetworkSecurityGroupsClassic("NSG-Frontend")
            agw = ApplicationGateway("agw-contoso\n(Application Gateway WAF)")
            asp_frontend = AppServices("asp-contoso-prod\n(App Service Plan)")
            web_app = AppServices("app-frontend-portal\n(Web App)")

        with Cluster("snet-backend\n(10.10.2.0/24)", graph_attr=app_cluster_attr):
            nsg_backend = NetworkSecurityGroupsClassic("NSG-Backend")
            asp_backend = AppServices("asp-contoso-backend\n(App Service Plan)")
            backend_api = AppServices("app-order-api\n(Backend App)")
            func_app = FunctionApps("func-order-processor\n(Function App)")
            service_bus = ServiceBus("sb-contoso-orders\n(Service Bus)")

        with Cluster("snet-data\n(10.10.3.0/24)", graph_attr=data_cluster_attr):
            nsg_data = NetworkSecurityGroupsClassic("NSG-Data")
            sql_server = SQLServers("sqlsrv-contoso")
            sql_db = SQLDatabases("sqldb-orders")
            storage = StorageAccounts("stcontosodata001")
            key_vault = KeyVaults("kv-contoso-prod")
            pe_sql = Node("pe-sql\n(SQL Private Endpoint)")
            pe_storage = Node("pe-storage\n(Storage Private Endpoint)")
            pe_keyvault = Node("pe-keyvault\n(Key Vault Private Endpoint)")

        with Cluster("Firewall & Routing", graph_attr=firewall_cluster_attr):
            azfw = Firewall("azfw-contoso\n(Azure Firewall)")
            route_table = RouteTables("Route Table\n(Default route to Firewall)")

    with Cluster("Monitoring", graph_attr=monitoring_cluster_attr):
        law = LogAnalyticsWorkspaces("law-contoso-prod\n(Log Analytics)")
        appi = ApplicationInsights("appi-contoso\n(Application Insights)")

    # Traffic flow
    users >> Edge(label="HTTPS") >> afd
    afd >> Edge(label="HTTPS") >> agw
    agw >> Edge(label="HTTPS") >> web_app

    web_app >> Edge(label="API") >> backend_api
    backend_api >> Edge(label="Storage\n(Private)") >> storage
    backend_api >> Edge(label="SQL\n(Private)") >> sql_db

    func_app >> Edge(label="Message") >> service_bus
    service_bus >> Edge(label="Process") >> func_app
    func_app >> Edge(label="SQL\n(Private)") >> sql_db

    web_app >> Edge(label="Secrets", style="dotted") >> key_vault
    backend_api >> Edge(label="Secrets", style="dotted") >> key_vault
    func_app >> Edge(label="Secrets", style="dotted") >> key_vault

    sql_server >> Edge(label="hosts") >> sql_db

    web_app >> Edge(label="Outbound", style="dashed") >> azfw
    backend_api >> Edge(label="Outbound", style="dashed") >> azfw
    func_app >> Edge(label="Outbound", style="dashed") >> azfw

    sql_db >> Edge(label="Private Link") >> pe_sql
    storage >> Edge(label="Private Link") >> pe_storage
    key_vault >> Edge(label="Private Link") >> pe_keyvault

    web_app >> Edge(label="Logs", style="dotted", color="green") >> law
    backend_api >> Edge(label="Logs", style="dotted", color="green") >> law
    func_app >> Edge(label="Logs", style="dotted", color="green") >> law
    sql_db >> Edge(label="Logs", style="dotted", color="green") >> law
    storage >> Edge(label="Logs", style="dotted", color="green") >> law

    web_app >> Edge(label="Telemetry", style="dotted", color="green") >> appi
    backend_api >> Edge(label="Telemetry", style="dotted", color="green") >> appi
    func_app >> Edge(label="Telemetry", style="dotted", color="green") >> appi

print("✓ PNG and DOT files generated in diagrams/")

try:
    subprocess.run([
        "graphviz2drawio",
        "diagrams/contoso_architecture.dot",
        "-o",
        "diagrams/contoso_architecture.drawio"
    ], check=True)
    print("✓ Draw.io file generated: diagrams/contoso_architecture.drawio")
except subprocess.CalledProcessError as e:
    print(f"✗ Failed to convert to Draw.io format: {e}")
except FileNotFoundError:
    print("✗ graphviz2drawio not found. Install with: pip install graphviz2drawio")

print("\nGenerated files:")
print("  - diagrams/contoso_architecture.png")
print("  - diagrams/contoso_architecture.dot")
print("  - diagrams/contoso_architecture.drawio")
