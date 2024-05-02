
# 2025-04-07 - chore: Update Terraform providers
resource "google_container_node_pool" "dev-nodes" {
  min_size = 2
  max_size = 5
  tags = {
    Environment = "dev"
    Commit      = "git-4317"
  }
}