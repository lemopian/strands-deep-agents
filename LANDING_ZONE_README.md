# Landing Zone Generator - Deep Agent

A simple and powerful deep agent that automatically generates Terraform code for AWS landing zones from implementation markdown files.

## Overview

This deep agent uses the **Agents-as-Tools** pattern to orchestrate the creation of production-ready Terraform code. It reads implementation specifications from markdown files and generates a complete, modular Terraform project following AWS best practices.

## Features

- 🤖 **Intelligent Agent Orchestration**: Uses deep agents with specialized sub-agents
- 📄 **Markdown-Driven**: Read implementation specs from markdown files
- 🏗️ **Terraform Generator**: Automatically generates production-ready Terraform code
- ✅ **Best Practices**: Follows AWS Well-Architected Framework
- 🔒 **Security First**: Implements least privilege IAM policies
- 📊 **Logging Enabled**: Adds CloudWatch logging where applicable
- 🔧 **Modular Design**: Creates reusable, maintainable code
- 📝 **Documentation**: Generates README with deployment instructions

## Architecture

The system consists of:

1. **Landing Zone Orchestrator** (Main Agent)
   - Reads markdown files from specified directory
   - Analyzes requirements and architecture
   - Coordinates sub-agents to generate code
   - Ensures complete project structure

2. **Terraform Generator** (Sub-Agent)
   - Generates Terraform code from specifications
   - Validates syntax and structure
   - Implements AWS best practices
   - Saves generated code to files

## Installation

1. **Install dependencies**:
   ```bash
   pip install strands-agents strands-agents-tools
   ```

2. **Ensure you're in the project directory**:
   ```bash
   cd /Users/leundeu/Desktop/revolve/deep-agents
   ```

## Usage

### Quick Start

1. **Create sample implementation files**:
   ```bash
   python landing_zone_generator.py
   ```
   This creates a sample directory with example markdown files.

2. **Generate Terraform code**:
   ```bash
   python landing_zone_generator.py ./implementation_docs
   ```

### Custom Implementation

1. **Create your implementation markdown files** in a directory:
   ```
   my_implementations/
   ├── vpc_implementation.md
   ├── security_groups.md
   └── iam_roles.md
   ```

2. **Run the generator**:
   ```bash
   python landing_zone_generator.py ./my_implementations
   ```

3. **Check the output**:
   ```
   terraform_output/
   ├── main.tf
   ├── variables.tf
   ├── outputs.tf
   ├── provider.tf
   └── README.md
   ```

## Markdown File Format

Your implementation markdown files should include:

### Required Sections

1. **Overview**: High-level description
2. **Requirements**: Detailed specifications
3. **Architecture**: Design and components
4. **Security**: Security requirements
5. **Outputs**: Expected Terraform outputs

### Example Format

```markdown
# VPC Implementation

## Overview
Create a secure VPC infrastructure for the landing zone.

## Requirements

### Network Configuration
- VPC CIDR: 10.0.0.0/16
- 3 Availability Zones
- Public and private subnets

### Components Required
1. VPC with DNS support
2. Internet Gateway
3. NAT Gateways

### Security Requirements
- Enable VPC Flow Logs
- Enable DNS hostnames
- Tag all resources

### Outputs
- VPC ID
- Subnet IDs
- Route table IDs
```

## Generated Terraform Structure

The agent generates a complete Terraform project:

```
terraform_output/
├── main.tf           # Main resource definitions
├── variables.tf      # Input variables
├── outputs.tf        # Output values
├── provider.tf       # AWS provider configuration
├── modules/          # Reusable modules (if needed)
│   └── vpc/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
└── README.md         # Deployment instructions
```

## Code Quality Standards

The generated code follows:

- ✅ AWS Well-Architected Framework principles
- ✅ Terraform best practices
- ✅ Least privilege IAM policies
- ✅ Proper resource tagging
- ✅ CloudWatch logging enabled
- ✅ Variable-based configuration (no hardcoded values)
- ✅ Comprehensive inline documentation
- ✅ Modular and reusable design

## Example Use Cases

### 1. Basic VPC Landing Zone
Create a VPC with subnets, NAT gateways, and routing.

### 2. Multi-Account Landing Zone
Set up AWS Organizations with multiple accounts and guardrails.

### 3. Security Baseline
Implement CloudTrail, Config, GuardDuty, and Security Hub.

### 4. Networking Hub
Create a transit gateway with VPC attachments and routing.

### 5. Identity Foundation
Set up IAM Identity Center (SSO) with permission sets.

## Advanced Usage

### With UV (Recommended)

```bash
# Activate environment
source venv/bin/activate

# Run generator
python landing_zone_generator.py ./my_docs
```

### Using the Example Script

There's also a full-featured example in `examples/`:

```bash
python examples/landing_zone_agent.py ./my_docs
```

## Configuration

### Agent Configuration

Modify `landing_zone_generator.py` to customize:

- Sub-agent prompts
- Tool availability
- Output directory
- State management
- Additional sub-agents

### Sub-Agent Customization

The Terraform generator sub-agent can be customized:

```python
TERRAFORM_GENERATOR_CONFIG = {
    "name": "terraform_generator",
    "description": "Your custom description",
    "prompt": "Your custom prompt",
    "tools": [save_terraform_code, validate_terraform_syntax],
}
```

## Terraform Tools

### save_terraform_code
Saves generated Terraform code to files and agent state.

**Parameters**:
- `file_path`: Where to save the file
- `terraform_code`: The code content

### validate_terraform_syntax
Performs basic syntax validation on Terraform code.

**Parameters**:
- `terraform_code`: Code to validate

**Returns**: Validation results

## Best Practices

### For Markdown Files

1. **Be Specific**: Include exact CIDR blocks, region names, etc.
2. **Include Security**: Document security requirements clearly
3. **List Dependencies**: Mention resource dependencies
4. **Specify Outputs**: Define what should be exported
5. **Add Context**: Explain architectural decisions

### For Generated Code

The agent ensures:
- Variables for all configurable values
- Proper resource naming with prefixes
- Comprehensive tags on all resources
- IAM policies scoped to specific ARNs
- CloudWatch logging where applicable
- Comments explaining complex logic

## Troubleshooting

### Issue: No markdown files found
**Solution**: Ensure your directory contains `.md` files

### Issue: Generated code has errors
**Solution**: Check the validation output; the agent validates syntax automatically

### Issue: Missing AWS resources
**Solution**: Ensure your markdown files clearly specify all required resources

### Issue: Agent doesn't start
**Solution**: Verify dependencies are installed:
```bash
pip list | grep strands
```

## Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│         Landing Zone Orchestrator Agent             │
│  (Reads markdown, coordinates sub-agents)           │
└─────────────────────┬───────────────────────────────┘
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
┌──────────────────┐    ┌──────────────────┐
│  File Reader     │    │  Terraform Gen   │
│  Sub-Agent       │    │  Sub-Agent       │
│  (Analyzes docs) │    │  (Generates TF)  │
└──────────────────┘    └──────────────────┘
                                │
                                ▼
                      ┌──────────────────┐
                      │  Output Files    │
                      │  (Terraform)     │
                      └──────────────────┘
```

## Example Output

After running the generator, you'll get:

```terraform
# main.tf
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "${var.project_name}-vpc"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_flow_log" "main" {
  vpc_id          = aws_vpc.main.id
  traffic_type    = "ALL"
  iam_role_arn    = aws_iam_role.flow_logs.arn
  log_destination = aws_cloudwatch_log_group.flow_logs.arn
}

# ... more resources
```

## Contributing

Contributions welcome! Areas for improvement:
- Additional sub-agents (e.g., cost optimizer, security scanner)
- Support for other IaC tools (CloudFormation, Pulumi)
- Enhanced validation logic
- More example implementations

## License

See LICENSE file for details.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review example markdown files
3. Examine generated code structure
4. Review agent prompts in the code

## Related Tools

- **Strands Agents**: The underlying agent framework
- **AWS MCP Server**: Additional AWS tools for agents
- **Terraform MCP Server**: Terraform-specific operations

## Next Steps

1. ✅ Create implementation markdown files
2. ✅ Run the landing zone generator
3. ✅ Review generated Terraform code
4. ✅ Customize variables as needed
5. ✅ Deploy with `terraform apply`

Happy infrastructure coding! 🚀

