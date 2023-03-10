data "azurerm_resource_group" "RG-dev" {
  name     = "devopsGTC"
}

resource "azurerm_kubernetes_cluster" "app" {
  name                = "gtcAKS"
  location            = data.azurerm_resource_group.RG-dev.location
  resource_group_name = data.azurerm_resource_group.RG-dev.name
  dns_prefix = "devopsgtc"
  sku_tier            = "Free"
  http_application_routing_enabled = true

  default_node_pool {
    name       = "default"
    node_count = 1
    vm_size    = "Standard_B2s"
    enable_auto_scaling = false
  }

  identity {
    type = "SystemAssigned"
  }

  tags = {
    Environment = "Development"
  }
}