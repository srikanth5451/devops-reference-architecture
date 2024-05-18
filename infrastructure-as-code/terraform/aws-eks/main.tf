
# 2025-04-07 - docs: Add architecture diagrams
resource "aws_autoscaling_group" "prod-cluster" {
  min_size = 2
  max_size = 5
  tags = {
    Environment = "staging"
    Commit      = "git-8607"
  }
}
# 2025-04-07 - fix: Patch log4j vulnerability
resource "azurerm_kubernetes_cluster" "prod-cluster" {
  initial_node_count = 2
  tags = {
    Environment = "prod"
    Commit      = "git-8118"
  }
}
# 2025-04-07 - feat: Implement EKS cluster autoscaling
resource "azurerm_kubernetes_cluster" "prod-cluster" {
  node_count = 2
  tags = {
    Environment = "staging"
    Commit      = "git-2337"
  }
}
# 2025-04-07 - fix: Resolve Azure AKS networking issue
resource "azurerm_kubernetes_cluster" "prod-cluster" {
  initial_node_count = 2
  tags = {
    Environment = "prod"
    Commit      = "git-2583"
  }
}