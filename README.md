# Strands DeepAgents

A planning-capable agent implementation using the [Strands Agents SDK](https://github.com/strands-agents/strands-agents), inspired by the DeepAgents pattern. This library enables sophisticated multi-agent systems with autonomous planning, sub-agent delegation, and persistent state management.

📖 **[Read the detailed blog post: DeepAgents Explained](https://www.pierreange.ai/blog/deepagents-explained)**

## Overview

Strands DeepAgents extends the [Strands Agents SDK](https://strandsagents.com/latest/documentation/docs/getting-started/) with advanced capabilities for building agents that can:

- **Plan and Execute**: Break down complex tasks into actionable TODO lists with automatic progress tracking
- **Delegate to Sub-Agents**: Create specialized sub-agents with custom tools and prompts for specific domains
- **Manage State**: Maintain conversation history, file system state, and persistent context across interactions
- **Operate Asynchronously**: Full support for async/await patterns for concurrent task execution

This implementation adapts concepts from [LangChain's DeepAgents](https://github.com/langchain-ai/deepagents) to work seamlessly with Strands' native architecture and tooling ecosystem.

## Capacities

### Core Capabilities

**Planning & Task Management**
- Automatic TODO list creation and tracking
- Multi-step task decomposition
- Progress monitoring with stateful persistence

**Sub-Agent Delegation**
- Create specialized agents for specific tasks (research, analysis, writing, etc.)
- Configure custom tools per sub-agent
- Model override per sub-agent for cost/performance optimization
- Parallel or sequential tool execution modes

**File System Operations**
- Virtual file system for agent workspace
- Read/write file operations
- Directory management
- Integration with `strands_tools` for extended capabilities

**Flexible Model Support**
- Amazon Bedrock (Claude, Titan, etc.)
- Anthropic, OpenAI, and other providers via Strands
- Per-agent model configuration

## Installation

### Prerequisites

- Python ≥3.12
- AWS credentials configured (for Bedrock models)
- Strands Agents SDK ≥0.1.0

### Install from Source

```bash
# Clone the repository
git clone https://github.com/your-username/strands-deepagents.git
cd strands-deepagents

# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

## Quick Start

```python
from strands_deepagents import create_deep_agent

# Create a deep agent with planning capabilities
agent = create_deep_agent(
    instructions="You are a helpful assistant that excels at planning and executing complex tasks.",
    model="global.anthropic.claude-sonnet-4-5-20250929-v1:0",
    subagents=[
        {
            "name": "research_agent",
            "description": "Specializes in researching and gathering information",
            "prompt": "You are a research specialist focused on finding accurate information.",
        },
        {
            "name": "writer_agent",
            "description": "Specializes in writing and content creation",
            "prompt": "You are a skilled writer focused on clear, engaging content.",
        }
    ],
)

# Execute a complex task
result = agent("""
Create a Python script that processes CSV files:
1. Read data from input.csv
2. Clean and validate the data
3. Generate a summary report
4. Save results to output.json

Please plan this task first, then execute.
""")

print(result)

# Check the agent's TODOs
todos = agent.state.get("todos")
for todo in todos:
    print(f"[{todo['status']}] {todo['content']}")
```

## Testing

### Run the Test Suite

```bash
# Activate virtual environment
source .venv/bin/activate

# Run all tests
pytest tests/

# Run specific test files
pytest tests/test_sub_agents.py
pytest tests/test_planning.py
pytest tests/test_factory.py

# Run with coverage
pytest --cov=strands_deepagents tests/

# Run async tests only
pytest -k "async" tests/
```

### Run Examples

```bash
# Activate virtual environment
source .venv/bin/activate

# Basic usage example
python examples/basic_usage.py

# Sub-agents example
python examples/sub_agents_example.py

# Sequential execution example
python examples/sequential_execution_example.py

# DeepSearch example (advanced)
python examples/deepsearch/agent.py
```

### Environment Setup

```bash
# Required: AWS credentials for Bedrock
export AWS_PROFILE=your-profile
export AWS_REGION=us-west-2

# Optional: Bypass tool consent for automated testing
export BYPASS_TOOL_CONSENT=true
```

## Strands-Specific Implementation

This implementation is tightly integrated with the Strands Agents SDK ecosystem:

### Native Strands Integration

**Agent Creation**
- Built on `strands.Agent` class as the core foundation
- Supports both synchronous (`agent()`) and asynchronous (`agent.invoke_async()`) invocation
- Access conversation history via `agent.messages` property
- Leverages custom `DeepAgentState` extending Strands' state management

**Tool System**
- Three approaches supported: function decorator, class-based tools, and module-based tools
- Built on `@tool` decorator from Strands SDK with automatic schema generation from docstrings and type hints
- Compatible with [`strands-agents-tools`](https://pypi.org/project/strands-agents-tools/) community package for pre-built tools
- Supports async tools with concurrent execution
- Tool streaming with progress updates via async generators
- `ToolContext` provides access to agent state, tool use data, and invocation state

**Model Providers**
- Native support for [Amazon Bedrock](https://docs.aws.amazon.com/bedrock/) via `BedrockModel` class (default provider)
- Additional providers: Anthropic, OpenAI, Cohere, LiteLLM, Ollama, SageMaker, and [custom providers](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/model-providers/custom_model_provider/)
- Unified interface across all providers through Strands' model abstraction
- Per-agent model configuration with runtime updates via `model.update_config()`
- Support for streaming, multimodal inputs, guardrails, and prompt caching

**State Management**
- Three types of state: **Conversation History** (agent.messages), **Agent State** (key-value storage), and **Request State** (per-invocation context)
- Agent state accessible via `agent.state.get()`, `agent.state.set()`, and `agent.state.delete()`
- JSON serialization validation ensures persistence compatibility
- Tools access state through `ToolContext` parameter
- Supports [session persistence](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/agents/session-management/) across application restarts
- Custom `DeepAgentState` adds: `todos`, `file_system`, `current_plan` fields

## Documentation & Resources

**Strands Agents**

- [Official Documentation](https://strandsagents.com/latest/)

**DeepAgents Pattern**
- [Blog: DeepAgents Explained](https://www.pierreange.ai/blog/deepagents-explained)
- [LangGraph DeepAgents (Original Implementation)](https://github.com/langchain-ai/deepagents)

## Examples

See the [`examples/`](./examples) directory for comprehensive usage examples:

- **`basic_usage.py`**: Simple agent with planning and file operations
- **`sub_agents_example.py`**: Multiple specialized sub-agents working together
- **`sequential_execution_example.py`**: Sequential task execution patterns
- **`deepsearch/`**: Advanced research agent with citations and internet search

## Architecture

```
┌─────────────────────────────────────────────┐
│           Main Deep Agent                   │
│  - Planning (TODO management)               │
│  - State persistence                        │
│  - Tool orchestration                       │
└─────────────┬───────────────────────────────┘
              │
              ├─► Planning Tools
              │   - create_todo
              │   - update_todo
              │   - list_todos
              │
              ├─► Task Tool (Sub-Agent Delegation)
              │   │
              │   ├─► Research Agent
              │   │   - Internet search tools
              │   │   - Citation extraction
              │   │
              │   ├─► Writer Agent
              │   │   - File operations
              │   │   - Content generation
              │   │
              │   └─► General Purpose Agent
              │       - Inherits all main agent tools
              │       - Flexible reasoning
              │
              └─► File System Tools
                  - read_file
                  - write_file
                  - list_directory
```

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Follow the coding standards (use `ruff` and `black` for formatting)
4. Add tests for new functionality
5. Update documentation as needed
6. Submit a pull request

## License

MIT License - see [LICENSE](./LICENSE) file for details.

## Acknowledgments

- **[Strands Agents Team](https://github.com/strands-agents)** for the foundational SDK and tooling ecosystem
- **[LangChain DeepAgents](https://github.com/langchain-ai/deepagents)** for the original DeepAgents pattern, prompts, and architectural inspiration
- The broader AI agents community for continued innovation
