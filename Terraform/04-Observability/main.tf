data "terraform_remote_state" "aks" {
  backend = "azurerm"
  config = {
    resource_group_name = "devopsGTC"
    storage_account_name = "storage4gtc"
    container_name = "backendterraform"
    key = "dev.terraform.tfstate"
   }
}


resource "helm_release" "datadog" {
  name = "datadog"
  chart = "datadog"
  repository = "https://helm.datadoghq.com"

  set {
    name = "datadog.apiKey"
    value = var.datadogApiKey
    type = "string"
  }
  values = [
    "${file("values/datadog-values.yaml")}"
  ]
}

resource "helm_release" "prometheus" {
  name = "prometheus"
  chart = "prometheus"
  repository = "https://prometheus-community.github.io/helm-charts"
  values = [ "${file("values/prometheus-values.yaml")}" ]
}

resource "helm_release" "grafana" {
  name = "grafana"
  chart = "grafana"
  repository = "https://grafana.github.io/helm-charts"
}

resource "helm_release" "signoz" {
  name = "signoz"
  chart = "signoz"
  repository = "https://charts.signoz.io"
}


