import os
import random
from datetime import datetime, timedelta
import subprocess
import textwrap

# Configuration
REPO_DIR = r"C:\Users\SRILUCKY\OneDrive\Desktop\my_github_projects\devops-reference-architecture"
USER_NAME = "Your Name"
USER_EMAIL = "your@email.com"
START_DATE = datetime(2024, 5, 1)
END_DATE = datetime(2024, 6, 30)

# Realistic DevOps commit messages
COMMIT_MESSAGES = [
    "feat: Implement EKS cluster autoscaling",
    "fix: Resolve Azure AKS networking issue",
    "chore: Update Terraform providers",
    "docs: Add architecture diagrams",
    "refactor: Simplify Kubernetes manifests",
    "feat(security): Add OPA gatekeeper policies",
    "fix(ci): Correct GitHub Actions workflow",
    "test: Add integration tests for payment service",
    "feat(monitoring): Configure Prometheus alerts",
    "chore: Upgrade Istio to 1.18.2",
    "fix: Patch log4j vulnerability",
    "feat: Implement blue-green deployments",
    "docs: Update disaster recovery plan",
    "refactor: Convert Pulumi to TypeScript",
    "fix(auth): Correct IAM role permissions"
]

# File templates with realistic changes
FILE_TEMPLATES = {
    "terraform": {
        "path": "infrastructure-as-code/terraform/{cloud}/main.tf",
        "content": """# {date} - {message}
resource "{resource_type}" "{name}" {{
  {config}
  tags = {{
    Environment = "{env}"
    Commit      = "{commit_hash}"
  }}
}}""",
        "vars": {
            "cloud": ["aws-eks", "azure-aks", "gcp-gke"],
            "resource_type": ["aws_autoscaling_group", "azurerm_kubernetes_cluster", "google_container_node_pool"],
            "name": ["prod-cluster", "dev-nodes", "canary-pool"],
            "config": [
                "min_size = {}\n  max_size = {}".format(random.randint(1,3), random.randint(3,6)),
                "node_count = {}".format(random.randint(2,4)),
                "initial_node_count = {}".format(random.randint(1,3))
            ],
            "env": ["prod", "staging", "dev"],
            "commit_hash": lambda: f"git-{random.randint(1000,9999)}"
        }
    },
    "kubernetes": {
        "path": "kubernetes/{component}/{file}",
        "content": """# {date} - {message}
apiVersion: {api_version}
kind: {kind}
metadata:
  name: {name}
spec:
  {config}""",
        "vars": {
            "component": ["argo-rollouts", "istio", "monitoring"],
            "file": ["canary.yaml", "virtualservice.yaml", "prometheus.yaml"],
            "api_version": ["argoproj.io/v1alpha1", "networking.istio.io/v1beta1", "monitoring.coreos.com/v1"],
            "kind": ["Rollout", "VirtualService", "Prometheus"],
            "name": ["frontend", "paymentservice", "monitoring"],
            "config": [
                "replicas: {}".format(random.randint(2,5)),
                "hosts:\n  - \"{}\"".format(random.choice(["api.prod.example.com", "web.staging.example.com"])),
                "scrapeInterval: {}".format(random.choice(["30s", "1m", "2m"]))
            ]
        }
    }
}

def setup_repo():
    """Initialize Git repository"""
    os.chdir(REPO_DIR)
    if not os.path.exists(".git"):
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "config", "user.name", USER_NAME], check=True)
        subprocess.run(["git", "config", "user.email", USER_EMAIL], check=True)
        print("Initialized new Git repository")
    else:
        print("Existing Git repository found")

def create_project_structure():
    """Create base directory structure"""
    dirs = [
        "infrastructure-as-code/terraform/aws-eks",
        "infrastructure-as-code/terraform/azure-aks",
        "kubernetes/argo-rollouts",
        "kubernetes/istio",
        "ci-cd/github-actions",
        "security/opa-policies"
    ]
    for d in dirs:
        os.makedirs(os.path.join(REPO_DIR, d), exist_ok=True)

def generate_file_change():
    """Generate realistic file modification"""
    template_type = random.choice(list(FILE_TEMPLATES.keys()))
    template = FILE_TEMPLATES[template_type]
    
    # Resolve template variables
    variables = {}
    for var, choices in template["vars"].items():
        variables[var] = choices() if callable(choices) else random.choice(choices)
    
    return template["path"].format(**variables), template["content"].format(
        date=datetime.now().strftime("%Y-%m-%d"),
        message=random.choice(COMMIT_MESSAGES),
        **variables
    )

def make_commit(commit_date, message):
    """Create a commit with backdated timestamp"""
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = commit_date.strftime("%Y-%m-%d %H:%M:%S")
    env["GIT_COMMITTER_DATE"] = env["GIT_AUTHOR_DATE"]
    
    # Generate and write file change
    file_path, content = generate_file_change()
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "a") as f:
        f.write("\n" + content)
    
    # Commit
    subprocess.run(["git", "add", file_path], check=True, env=env)
    subprocess.run(["git", "commit", "-m", message], check=True, env=env)
    print(f"Commit: {commit_date.strftime('%Y-%m-%d')} - {message}")

def generate_commits():
    """Generate commit history between May-June 2024"""
    current_date = START_DATE
    while current_date <= END_DATE:
        # Skip some weekends (30% chance)
        if current_date.weekday() >= 5 and random.random() < 0.3:
            current_date += timedelta(days=1)
            continue
            
        # 1-3 commits per weekday
        for _ in range(random.randint(1, 3)):
            commit_time = current_date.replace(
                hour=random.randint(9, 18),  # Business hours
                minute=random.randint(0, 59)
            )
            make_commit(commit_time, random.choice(COMMIT_MESSAGES))
        
        current_date += timedelta(days=1)

def main():
    print(f"Generating DevOps commits ({START_DATE.date()} to {END_DATE.date()})")
    setup_repo()
    create_project_structure()
    
    # Initial commit if empty repo
    if not subprocess.run(["git", "rev-list", "--all"], capture_output=True).stdout:
        make_commit(START_DATE, "chore: Initial project setup")
    
    generate_commits()
    
    print("\nVerification commands:")
    print("git log --oneline --graph --all")
    print("\nTo push to GitHub:")
    print("git remote add origin YOUR_REPO_URL")
    print("git push -u origin main --force")

if __name__ == "__main__":
    main()