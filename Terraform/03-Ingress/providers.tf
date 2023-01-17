provider "azurerm" {
  features {}
}

terraform {
  required_providers {
    helm = {
      source  = "hashicorp/helm"
      version = "~>2.8.0"

    }
  }
   backend "azurerm" {
    resource_group_name = "devopsGTC"
    storage_account_name = "storage4gtc"
    container_name = "backendterraform"
    key = "ingress.terraform.tfstate"
  }
}