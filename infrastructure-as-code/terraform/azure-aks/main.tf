
# 2025-04-07 - chore: Update Terraform providers
resource "google_container_node_pool" "dev-nodes" {
  min_size = 2
  max_size = 5
  tags = {
    Environment = "dev"
    Commit      = "git-4317"
  }
}
# 2025-04-07 - fix(auth): Correct IAM role permissions
resource "aws_autoscaling_group" "canary-pool" {
  node_count = 2
  tags = {
    Environment = "staging"
    Commit      = "git-4746"
  }
}