# Strands DeepAgents

Create planning-capable AI agents with sub-agent delegation and file system operations, built on the [Strands Agents SDK](https://github.com/strands-ai/strands-agents).

## What is DeepAgents?

![DeepAgents Overview](./docs/img/deep-agent-overview.png)

DeepAgents enables AI agents to handle complex, multi-step tasks by combining:
- 🧠 **Planning** - Break tasks into TODO lists
- 📁 **File Operations** - Read, write, and edit files
- 🤝 **Sub-agent Delegation** - Specialized agents for specific tasks
- 💾 **Session Persistence** - Resume work across sessions

Check the related [article](http://pierreange.ai/blog/deep-agents-using-strands) for more details.

## Installation

```bash
# Using UV (recommended)
uv pip install strands-deepagents

# Using pip
pip install strands-deepagents
```

**Requirements:** Python >= 3.12

## Quick Start

### Basic Agent

```python
from strands_deep_agents import create_deep_agent

agent = create_deep_agent(
    instructions="You are a helpful coding assistant.",
    model="global.anthropic.claude-sonnet-4-5-20250929-v1:0"
)

result = agent("Create a Python calculator module with add, subtract, multiply, divide functions")
print(result)
```

The agent will automatically:
1. Plan the task using TODOs
2. Create the file with proper structure
3. Add docstrings and examples

### Check Task Progress

```python
# View the agent's planned tasks
for todo in agent.state.get("todos", []):
    print(f"[{todo['status']}] {todo['content']}")
```

Output:
```
[completed] Plan calculator module structure
[completed] Create calculator.py file
[completed] Add arithmetic functions
[completed] Add docstrings and examples
```

## Usage Patterns

### 1. File Operations

The agent has built-in file tools:

```python
agent = create_deep_agent(
    instructions="You are a code reviewer."
)

# Agent can read files
result = agent("Review the code in calculator.py and suggest improvements")

# Agent can write files
result = agent("Create a requirements.txt file with necessary dependencies")

# Agent can edit files
result = agent("Add type hints to all functions in calculator.py")
```

### 2. Sub-agent Delegation

Create specialized sub-agents for specific tasks:

```python
# Define specialized sub-agents
subagents = [
    {
        "name": "code_reviewer",
        "description": "Expert at reviewing code for quality and best practices",
        "prompt": "You are a senior code reviewer. Focus on readability, performance, and security."
    },
    {
        "name": "test_writer",
        "description": "Creates comprehensive unit tests with edge cases",
        "prompt": "You are a testing expert. Write thorough pytest tests with fixtures and parametrization."
    },
    {
        "name": "doc_writer",
        "description": "Writes clear documentation and docstrings",
        "prompt": "You are a technical writer. Create clear, concise documentation."
    }
]

agent = create_deep_agent(
    instructions="You are a senior software developer.",
    subagents=subagents
)

# The main agent will delegate to sub-agents automatically
result = agent("""
Create a user authentication module with:
1. Login and logout functions
2. Unit tests
3. Full documentation

Use sub-agents where appropriate.
""")
```

The main agent will:
- Create the authentication module
- Call `test_writer` sub-agent to generate tests
- Call `doc_writer` sub-agent for documentation
- Call `code_reviewer` sub-agent to review everything

### 3. Session Persistence

Save and restore agent state across sessions:

```python
from strands_deep_agents import create_deep_agent
from strands.session.file_session_manager import FileSessionManager

# First session - start a project
session_manager = FileSessionManager(
    session_id="project-xyz",
    storage_dir="./sessions"
)

agent = create_deep_agent(
    instructions="You are a full-stack developer.",
    session_manager=session_manager
)

agent("Start building a REST API for a todo app")
# Agent creates files, plans tasks...

# Later - resume the same project
session_manager = FileSessionManager(
    session_id="project-xyz",  # Same ID
    storage_dir="./sessions"
)

agent = create_deep_agent(
    instructions="You are a full-stack developer.",
    session_manager=session_manager
)

# Conversation history and TODOs are restored
agent("Continue where we left off. Add authentication to the API")
```

#### S3 Session Storage

For cloud-based persistence:

```python
from strands.session.s3_session_manager import S3SessionManager

session_manager = S3SessionManager(
    session_id="user-123",
    bucket_name="my-agent-sessions",
    prefix="agents/"
)

agent = create_deep_agent(
    instructions="You are a helpful assistant.",
    session_manager=session_manager
)
```

### 4. Async Operations

For parallel execution and better performance:

```python
import asyncio
from strands_deep_agents import async_create_deep_agent

async def main():
    agent = await async_create_deep_agent(
        instructions="You are a data analyst.",
        model="global.anthropic.claude-sonnet-4-5-20250929-v1:0"
    )

    result = await agent.invoke_async(
        "Analyze the CSV files in ./data and create a summary report"
    )
    print(result)

asyncio.run(main())
```

### 5. Custom Tools

Add your own tools to the agent:

```python
from strands import tool

@tool
def fetch_weather(city: str) -> str:
    """Get current weather for a city."""
    # Your implementation
    return f"Weather in {city}: Sunny, 72°F"

@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email."""
    # Your implementation
    return f"Email sent to {to}"

agent = create_deep_agent(
    instructions="You are a personal assistant.",
    tools=[fetch_weather, send_email]
)

result = agent("Check weather in San Francisco and email me a summary")
```

### 6. Sequential Execution

Force sequential tool execution (useful for debugging):

```python
agent = create_deep_agent(
    instructions="You are a helpful assistant.",
    disable_parallel_tool_calling=True  # Tools execute one at a time
)

result = agent("Create three files: config.py, main.py, and utils.py")
# Files will be created sequentially instead of in parallel
```

### 7. Multi-step Workflows

Agents excel at complex, multi-step tasks:

```python
agent = create_deep_agent(
    instructions="You are a Python package developer.",
    subagents=[
        {
            "name": "architect",
            "description": "Designs project structure and architecture",
            "prompt": "You are a software architect. Design clean, scalable structures."
        },
        {
            "name": "implementer",
            "description": "Implements code based on specifications",
            "prompt": "You are a senior developer. Write clean, efficient code."
        },
        {
            "name": "tester",
            "description": "Creates comprehensive tests",
            "prompt": "You are a QA engineer. Write thorough tests."
        }
    ]
)

result = agent("""
Create a Python package called 'api_client' with:
- Modular structure (src/ layout)
- HTTP client with retry logic
- Error handling
- Comprehensive tests
- README with examples
- pyproject.toml configuration

Plan this properly and delegate to sub-agents where appropriate.
""")
```

## Common Use Cases

### Code Development

```python
agent = create_deep_agent(
    instructions="You are an expert Python developer.",
    subagents=[
        {
            "name": "code_reviewer",
            "description": "Reviews code quality",
            "prompt": "Review for readability, performance, and best practices."
        }
    ]
)

# The agent can handle the full development lifecycle
result = agent("Create a Flask REST API with CRUD operations for a blog")
```

### Research & Documentation

```python
agent = create_deep_agent(
    instructions="You are a technical researcher and writer.",
    tools=[web_search_tool]  # Add your search tool
)

result = agent("""
Research best practices for FastAPI deployment and create a
comprehensive guide with examples.
""")
```

### Refactoring

```python
agent = create_deep_agent(
    instructions="You are a refactoring expert."
)

result = agent("""
Refactor the legacy code in ./src:
1. Add type hints
2. Break up large functions
3. Improve naming
4. Add docstrings
5. Create tests
""")
```

### Data Processing

```python
agent = create_deep_agent(
    instructions="You are a data engineer."
)

result = agent("""
Process the CSV files in ./data:
1. Clean and validate data
2. Transform to normalized format
3. Generate summary statistics
4. Create visualization script
5. Export to JSON
""")
```

## API Reference

### `create_deep_agent()`

Create a synchronous deep agent.

```python
agent = create_deep_agent(
    tools=None,                           # Additional custom tools
    instructions="",                      # System instructions
    model=None,                          # Model ID (default: Claude Sonnet 4)
    subagents=None,                      # List of sub-agent configs
    initial_state=None,                  # Initial state dict
    disable_parallel_tool_calling=False, # Force sequential execution
    session_manager=None,                # For persistence
    **kwargs                             # Additional Agent params
)
```

**Returns:** `Agent` instance

### `async_create_deep_agent()`

Create an asynchronous deep agent (same parameters as `create_deep_agent`).

```python
agent = await async_create_deep_agent(
    instructions="You are a helpful assistant.",
    model="global.anthropic.claude-sonnet-4-5-20250929-v1:0"
)

result = await agent.invoke_async("Your task here")
```

### Sub-agent Configuration

```python
subagent = {
    "name": "unique_name",           # Identifier
    "description": "When to use this agent",  # Helps main agent decide
    "prompt": "System prompt for sub-agent",  # Instructions
    "tools": [...],                  # Optional: specific tools
    "model": "model-id",            # Optional: override model
}
```

## Configuration

### Environment Variables

```bash
# AWS Bedrock
export AWS_REGION=us-east-1
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret

# Optional: Skip tool consent prompts
export BYPASS_TOOL_CONSENT=true
```

### Model Options

```python
# AWS Bedrock models
agent = create_deep_agent(
    model="global.anthropic.claude-sonnet-4-5-20250929-v1:0"
)

# Custom model configuration
from strands.models import Model

custom_model = Model(
    provider="bedrock",
    name="claude-3-5-sonnet-20241022-v2:0",
    region="us-east-1"
)

agent = create_deep_agent(model=custom_model)
```

## Examples

The `examples/` directory contains ready-to-run demonstrations:

```bash
# Basic usage
python examples/basic_usage.py

# Sub-agent patterns
python examples/sub_agents.py

# Session persistence
python examples/session_persistence.py

# Sequential execution
python examples/sequential_execution.py

# Advanced research agent
cd examples/deepsearch
python agent.py
```

## Best Practices

1. **Write Clear Instructions** - Be specific about what the agent should do
2. **Use Sub-agents for Specialization** - Delegate complex subtasks to focused agents
3. **Enable Planning** - Let the agent break down complex tasks
4. **Leverage Context Quarantine** - Use sub-agents to isolate subtasks and prevent context pollution
5. **Save State** - Use session persistence for long-running projects
6. **Sequential for Debugging** - Use `disable_parallel_tool_calling=True` when debugging

## Troubleshooting

### Agent not creating TODOs
Explicitly ask for planning: "Create a plan first, then execute"

### Sub-agent not being called
Make sub-agent descriptions specific and relevant to the task

### State not persisting
Ensure `session_manager` is provided and `session_id` is consistent


## Links

- **GitHub**: https://github.com/lemopian/strands-deep-agents
- **Strands Agents SDK**: https://github.com/strands-agents/sdk-python
- **Inspiration**: https://github.com/langchain-ai/deepagents
-
## License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Built with ❤️ by PA**
