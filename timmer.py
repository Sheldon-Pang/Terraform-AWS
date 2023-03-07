import os
import subprocess
import time

# Define the Terraform command to run
terraform_command = "terraform"

# CHANGE THIS
# Defines the directory where the Terraform configuration is located
terraform_dir = "/path/to/terraform/config"

# Define the timeout in seconds
timeout = 300  # 5 minutes

# Define the Terraform commands to run
terraform_commands = [
    "plan",
    "apply -auto-approve",
    "destroy -auto-approve"
]

# Change the current working directory to the Terraform directory
os.chdir(terraform_dir)

# Run each Terraform command and wait for 5 minutes before destroying
for command in terraform_commands:
    print(f"[+]Running command: {command}")
    subprocess.run(terraform_command + " " + command, check=True, shell=True)
    if command.startswith("apply -auto-approve"):
        print(f"Waiting for {timeout} seconds before destroying infrastructure...")
        for remaining in range(timeout, 0, -10):
            print(f"Time remaining: {remaining} seconds")
            time.sleep(10)
