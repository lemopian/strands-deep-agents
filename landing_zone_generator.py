#!/usr/bin/env python3
"""
Simple Landing Zone Generator using Deep Agents.

This script creates a deep agent that reads implementation markdown files
and generates Terraform code for AWS landing zones.

Usage:
    python landing_zone_generator.py <markdown_files_directory>

Example:
    python landing_zone_generator.py ./implementation_docs
"""

import os
import sys
from pathlib import Path
from strands_deepagents import create_deep_agent
from strands_deepagents.types import SubAgent
from strands_deepagents.tools import save_terraform_code, validate_terraform_syntax


# Terraform Generator Sub-Agent Configuration
TERRAFORM_GENERATOR_CONFIG = {
    "name": "terraform_generator",
    "description": (
        "Expert Terraform code generator for AWS infrastructure. "
        "Converts specifications into production-ready Terraform code following AWS best practices. "
        "Handles IAM policies, logging, tagging, and modular design."
    ),
    "prompt": """You are an expert Terraform code generator for AWS landing zones.

Core Responsibilities:
- Generate production-ready Terraform code from specifications
- Follow AWS Well-Architected Framework principles
- Implement proper IAM policies with least privilege
- Enable CloudWatch logging for all applicable resources
- Use variables instead of hardcoded values
- Create modular, reusable code

Best Practices:
- Use proper provider version constraints
- Implement remote state configuration
- Add comprehensive variable descriptions
- Create meaningful outputs
- Follow Terraform naming conventions
- Add inline comments where necessary
- Validate code structure before saving

Always save generated code using the save_terraform_code tool and validate it.""",
    "tools": [save_terraform_code, validate_terraform_syntax],
}


def create_landing_zone_deep_agent(files_directory: str):
    """
    Create a deep agent for landing zone generation from markdown files.

    Args:
        files_directory: Path to directory containing implementation markdown files

    Returns:
        Configured deep agent instance
    """
    # Validate directory
    if not os.path.exists(files_directory):
        raise ValueError(f"Directory does not exist: {files_directory}")

    # Convert to absolute path
    abs_dir = os.path.abspath(files_directory)

    # Configure the terraform generator sub-agent
    terraform_subagent = SubAgent(
        name=TERRAFORM_GENERATOR_CONFIG["name"],
        description=TERRAFORM_GENERATOR_CONFIG["description"],
        prompt=TERRAFORM_GENERATOR_CONFIG["prompt"],
        tools=TERRAFORM_GENERATOR_CONFIG["tools"],
    )

    # Main agent instructions
    instructions = f"""You are a Landing Zone Orchestrator specialized in AWS infrastructure.

Your mission: Create Terraform-based AWS landing zones from implementation markdown files.

Source Directory: {abs_dir}

Workflow:
1. Scan and read all markdown files in the source directory
2. Analyze requirements, architecture, and AWS services needed
3. Design a modular Terraform structure
4. Use the terraform_generator sub-agent to create Terraform code for each component
5. Generate a complete, deployable Terraform project

Project Structure to Create:
- main.tf (main resources)
- variables.tf (input variables)
- outputs.tf (output values)
- provider.tf (provider configuration)
- modules/ (reusable modules if needed)
- README.md (deployment instructions)

Key Requirements:
- Use explicit argument passing everywhere
- Follow least privilege for IAM policies
- Enable logging for all resources that support it
- Use variables for flexibility (avoid hardcoded values)
- Add proper resource tagging
- Include security best practices
- Ensure modular and reusable code

Output Directory: Create terraform code in ./terraform_output/"""

    # Create and return the deep agent
    agent = create_deep_agent(
        instructions=instructions,
        subagents=[terraform_subagent],
        initial_state={
            "todos": [],
            "files": {},
            "source_directory": abs_dir,
        },
    )

    return agent


def create_sample_implementation_doc(directory: str) -> str:
    """
    Create a sample implementation markdown file for demonstration.

    Args:
        directory: Directory where to create the sample file

    Returns:
        Path to the created sample file
    """
    os.makedirs(directory, exist_ok=True)

    sample_file = os.path.join(directory, "vpc_and_subnets.md")

    sample_content = """# AWS Landing Zone - VPC and Networking Implementation

## Overview
Implement a secure, multi-AZ VPC infrastructure as the foundation for the AWS landing zone.

## Architecture Requirements

### VPC Configuration
- **VPC CIDR Block**: 10.0.0.0/16
- **Region**: us-east-1 (configurable via variable)
- **DNS Support**: Enabled
- **DNS Hostnames**: Enabled

### Subnet Design
Deploy across 3 Availability Zones for high availability:

**Public Subnets** (Internet-facing):
- us-east-1a: 10.0.1.0/24
- us-east-1b: 10.0.2.0/24
- us-east-1c: 10.0.3.0/24

**Private Subnets** (Internal):
- us-east-1a: 10.0.11.0/24
- us-east-1b: 10.0.12.0/24
- us-east-1c: 10.0.13.0/24

### Network Components

#### Internet Gateway
- Attach to VPC for public internet access
- Required for public subnets

#### NAT Gateways
- Deploy one NAT Gateway per Availability Zone
- Place in public subnets
- Allocate Elastic IPs for each NAT Gateway
- Enable private subnets to access internet

#### Route Tables

**Public Route Table**:
- Default route (0.0.0.0/0) → Internet Gateway
- Associate with all public subnets

**Private Route Tables** (one per AZ):
- Default route (0.0.0.0/0) → NAT Gateway in same AZ
- Associate with corresponding private subnet

### Security Requirements

#### VPC Flow Logs
- Enable VPC Flow Logs
- Send logs to CloudWatch Logs
- Log all traffic (ACCEPT and REJECT)
- Create IAM role with permissions to write to CloudWatch

#### Network ACLs
- Use default NACL with all traffic allowed
- Can be customized based on security requirements

#### Tags
All resources must be tagged with:
- Environment (e.g., "production", "staging")
- Project (e.g., "landing-zone")
- ManagedBy (e.g., "terraform")

## Terraform Requirements

### Variables Required
- `environment` - Environment name
- `project_name` - Project identifier
- `vpc_cidr` - VPC CIDR block
- `aws_region` - AWS region
- `availability_zones` - List of AZs to use
- `public_subnet_cidrs` - List of public subnet CIDRs
- `private_subnet_cidrs` - List of private subnet CIDRs

### Outputs Required
- `vpc_id` - VPC identifier
- `vpc_cidr` - VPC CIDR block
- `public_subnet_ids` - List of public subnet IDs
- `private_subnet_ids` - List of private subnet IDs
- `nat_gateway_ids` - List of NAT Gateway IDs
- `internet_gateway_id` - Internet Gateway ID

## IAM Permissions

### CloudWatch Logs Role
Create IAM role for VPC Flow Logs with policy allowing:
- `logs:CreateLogGroup`
- `logs:CreateLogStream`
- `logs:PutLogEvents`
- `logs:DescribeLogGroups`
- `logs:DescribeLogStreams`

Scope to specific log group ARN for least privilege.

## Implementation Notes
- Use `aws_vpc`, `aws_subnet`, `aws_internet_gateway` resources
- Use `aws_nat_gateway` with `aws_eip` for NAT
- Use `aws_route_table` and `aws_route_table_association` for routing
- Use `aws_flow_log` for VPC flow logs
- Use `aws_cloudwatch_log_group` for log storage
"""

    with open(sample_file, "w") as f:
        f.write(sample_content)

    return sample_file


def main():
    """
    Main entry point for the landing zone generator.
    """
    print("=" * 80)
    print("AWS Landing Zone Generator - Deep Agent")
    print("=" * 80)
    print()

    # Get directory from command line argument
    if len(sys.argv) < 2:
        print("Usage: python landing_zone_generator.py <markdown_files_directory>")
        print()

        # Create sample directory and file
        sample_dir = "./implementation_docs"
        print(f"No directory specified. Creating sample directory: {sample_dir}")

        sample_file = create_sample_implementation_doc(sample_dir)
        print(f"Created sample implementation file: {sample_file}")
        print()
        print("Now run the script with the sample directory:")
        print(f"  python landing_zone_generator.py {sample_dir}")
        print()
        sys.exit(0)

    files_dir = sys.argv[1]

    # Validate directory exists
    if not os.path.exists(files_dir):
        print(f"Error: Directory '{files_dir}' does not exist.")
        print()
        print("Please provide a valid directory containing markdown implementation files.")
        sys.exit(1)

    # Check for markdown files
    md_files = list(Path(files_dir).glob("*.md"))
    if not md_files:
        print(f"Warning: No markdown files found in '{files_dir}'")
        print()
    else:
        print(f"Found {len(md_files)} markdown file(s) in '{files_dir}':")
        for f in md_files:
            print(f"  - {f.name}")
        print()

    # Create the deep agent
    print("Initializing Landing Zone Deep Agent...")
    agent = create_landing_zone_deep_agent(files_dir)
    print("Agent initialized successfully!")
    print()

    # Prepare output directory
    output_dir = "./terraform_output"
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output directory: {output_dir}")
    print()

    # Run the agent
    print("Starting landing zone generation...")
    print("-" * 80)

    task_description = f"""
Read all implementation markdown files from '{files_dir}' and generate a complete 
Terraform landing zone implementation.

Tasks:
1. Read and analyze all markdown files in the directory
2. Extract AWS services, resources, and requirements
3. Design a modular Terraform structure
4. Generate Terraform code for each component:
   - main.tf with all resources
   - variables.tf with all configurable parameters
   - outputs.tf with important output values
   - provider.tf with AWS provider configuration
5. Save all files to the {output_dir} directory
6. Create a README.md with deployment instructions

Ensure all code follows AWS best practices, uses variables for flexibility,
implements proper IAM permissions, and enables logging where applicable.
"""

    result = agent(task_description)

    print()
    print("-" * 80)
    print("GENERATION COMPLETE")
    print("=" * 80)
    print()
    print("Result:")
    print(result)
    print()
    print("=" * 80)
    print(f"Check the {output_dir} directory for generated Terraform files.")
    print()


if __name__ == "__main__":
    main()
