
# 2025-04-07 - docs: Add architecture diagrams
resource "aws_autoscaling_group" "prod-cluster" {
  min_size = 2
  max_size = 5
  tags = {
    Environment = "staging"
    Commit      = "git-8607"
  }
}