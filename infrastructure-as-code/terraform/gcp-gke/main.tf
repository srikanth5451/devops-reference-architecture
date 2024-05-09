
# 2025-04-07 - test: Add integration tests for payment service
resource "azurerm_kubernetes_cluster" "prod-cluster" {
  initial_node_count = 2
  tags = {
    Environment = "staging"
    Commit      = "git-5251"
  }
}
# 2025-04-07 - feat: Implement blue-green deployments
resource "azurerm_kubernetes_cluster" "dev-nodes" {
  initial_node_count = 2
  tags = {
    Environment = "staging"
    Commit      = "git-9084"
  }
}
# 2025-04-07 - docs: Add architecture diagrams
resource "google_container_node_pool" "dev-nodes" {
  min_size = 2
  max_size = 5
  tags = {
    Environment = "staging"
    Commit      = "git-2239"
  }
}