# Strands Deep Agents

Build sophisticated AI agent systems with planning, sub-agent delegation, and multi-step workflows. Built on the [Strands Agents SDK](https://github.com/strands-ai/strands-agents).

## What is Deep Agents?

![Deep Agents Overview](https://raw.githubusercontent.com/lemopian/strands-deep-agents/main/docs/img/deep-agent-overview.png)

Deep Agents enables AI systems to handle complex, multi-step tasks through:
- 🧠 **Strategic Planning** - Break down complex tasks into actionable TODOs
- 🤝 **Sub-agent Orchestration** - Delegate specialized tasks to focused agents
- 📁 **Context Management** - Efficient file-based operations to keep context lean
- 💾 **Session Persistence** - Resume work across sessions
- 🔬 **Research & Analysis** - Multi-perspective investigation and synthesis

**Featured Example**: [DeepSearch](#deepsearch-advanced-research-agent) - A production-ready research agent demonstrating sub-agent orchestration, parallel research, and intelligent synthesis.

Check the related [article](http://pierreange.ai/blog/deep-agents-using-strands) for more details.

## Installation

```bash
# Using UV
uv add strands-deep-agents

# Using pip
pip install strands-deep-agents
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

## DeepSearch: Advanced Research Agent

DeepSearch demonstrates the full power of Deep Agents through a production-ready research agent system with intelligent orchestration and parallel research capabilities.

For this example, we can use any internet search tool, for example [Linkup] (https://app.linkup.so/) or tavily tool for web search.

### Architecture

DeepSearch uses a **three-tier agent architecture**:

1. **Research Lead Agent** - Strategic planning, task decomposition, and synthesis
2. **Research Sub-agents** - Parallel, focused investigation on specific topics
3. **Citations Agent** - Post-processing to add proper source references

### Key Features

- **Intelligent Task Decomposition**: Analyzes queries as depth-first (multiple perspectives) or breadth-first (independent sub-questions)
- **Parallel Research**: Deploys multiple sub-agents simultaneously for efficient information gathering
- **Context Management**: Sub-agents write findings to files, keeping context lean
- **Source Citation**: Automated citation agent adds proper references to final reports
- **Session Persistence**: Resume research across sessions

### Running DeepSearch

```bash
cd examples/deepsearch

# Basic usage with default prompt
python agent.py

# Custom research prompt
python agent.py -p "Research the impact of AI on healthcare in 2025"
```

### DeepSearch Implementation

```python
from strands_deep_agents import create_deep_agent, SubAgent
from strands_tools import tavily, file_read, file_write

# Research sub-agent - performs focused investigations
research_subagent = SubAgent(
    name="research_subagent",
    description=(
        "Specialized research agent for focused investigations. "
        "Researches specific questions, gathers facts, analyzes sources. "
        "Has access to web search. Writes findings to files."
    ),
    tools=[tavily, file_write],
    prompt="You are a thorough researcher. Gather comprehensive, accurate information..."
)

# Citations agent - adds source references
citations_agent = SubAgent(
    name="citations_agent",
    description="Adds proper citations to research reports.",
    tools=[file_read, file_write],
    prompt="Add citations to research text using provided sources..."
)

# Create the research lead agent
agent = create_deep_agent(
    instructions="""
    You are an expert research lead. Your role:
    1. Analyze the research question
    2. Create a research plan
    3. Deploy research sub-agents for focused investigations
    4. Synthesize findings into a comprehensive report
    5. Call citations agent to add references
    """,
    subagents=[research_subagent, citations_agent],
    tools=[file_read, file_write]
)

# Execute research
result = agent("""
Research AI safety in 2025:
1. Main challenges and concerns
2. Leading organizations and initiatives
Create a comprehensive report with executive summary.
""")
```

### How DeepSearch Works

1. **Planning Phase**: Lead agent analyzes the query and creates a research plan
2. **Parallel Research**: Multiple research sub-agents investigate different aspects simultaneously
3. **File-Based Context**: Sub-agents write findings to `./research_findings_*.md` files
4. **Synthesis**: Lead agent reads all findings and synthesizes a comprehensive report
5. **Citations**: Citations agent adds proper source references to the final report

### Example Output Structure

```
Research findings written to: research_findings_1.md, research_findings_2.md, ...
Final report: ai_safety_2025_report.md

TODOs:
✅ Analyze research question and create plan
✅ Deploy subagent: AI safety challenges
✅ Deploy subagent: Leading organizations
✅ Deploy subagent: Recent initiatives
✅ Synthesize findings into report
✅ Add citations to report
```

## Core Patterns

### Sub-agent Delegation

Deep Agents excel at delegating specialized tasks:

```python
from strands_deep_agents import create_deep_agent

subagents = [
    {
        "name": "researcher",
        "description": "Conducts focused research on specific topics",
        "prompt": "You are a thorough researcher. Gather comprehensive information."
    },
    {
        "name": "analyst",
        "description": "Analyzes data and identifies patterns",
        "prompt": "You are a data analyst. Find insights and patterns."
    }
]

agent = create_deep_agent(
    instructions="You are a research coordinator.",
    subagents=subagents
)
```

### Session Persistence

Resume work across sessions:

```python
from strands.session.file_session_manager import FileSessionManager

session_manager = FileSessionManager(
    session_id="project-xyz",
    storage_dir="./sessions"
)

agent = create_deep_agent(
    instructions="You are a research assistant.",
    session_manager=session_manager
)

# First session
agent("Start researching quantum computing")

# Later - conversation history and TODOs restored
agent("Continue where we left off")
```

### Custom Tools

Extend agents with your own tools:

```python
from strands import tool

@tool
def web_search(query: str) -> str:
    """Search the web for information."""
    # Your implementation
    return search_results

agent = create_deep_agent(
    instructions="You are a research assistant.",
    tools=[web_search]
)
```

## API Reference

### `create_deep_agent()`

Create a deep agent with planning and sub-agent capabilities.

```python
from strands_deep_agents import create_deep_agent

agent = create_deep_agent(
    instructions="System prompt for the agent",
    model=None,                          # Default: Claude Sonnet 4
    subagents=None,                      # List of SubAgent configs
    tools=None,                          # Additional custom tools
    session_manager=None,                # For persistence
    disable_parallel_tool_calling=False, # Force sequential execution
    **kwargs                             # Additional Agent params
)
```

### `SubAgent`

Define specialized sub-agents:

```python
from strands_deep_agents import SubAgent

subagent = SubAgent(
    name="unique_name",
    description="When to use this agent (helps main agent decide)",
    prompt="System prompt for sub-agent",
    tools=[...],     # Optional: specific tools
    model=model      # Optional: override model
)
```

### Async Support

```python
from strands_deep_agents import async_create_deep_agent

agent = await async_create_deep_agent(
    instructions="You are a research assistant."
)
result = await agent.invoke_async("Your task")
```

## Configuration

### Environment Variables

```bash
# AWS Bedrock (default provider)
export AWS_REGION=us-east-1
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret

# Optional: Skip tool consent prompts
export BYPASS_TOOL_CONSENT=true
```

### Model Options

```python
# Use AWS Bedrock models (default)
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

## Additional Examples

The `examples/` directory contains more patterns:

```bash
# Basic agent usage
python examples/basic_usage.py

# Sub-agent delegation patterns
python examples/sub_agents.py

# Session persistence
python examples/session_persistence.py

# DeepSearch - Advanced research agent (recommended)
cd examples/deepsearch
python agent.py
```

## Best Practices

1. **Clear Instructions** - Be specific about agent roles and expectations
2. **Strategic Sub-agents** - Use sub-agents for specialized, focused tasks
3. **Context Management** - Use file operations to keep context lean
4. **Session Persistence** - Enable for long-running or resumable tasks
5. **Prompt for Planning** - Encourage agents to create plans before execution


## Links

- **GitHub**: https://github.com/lemopian/strands-deep-agents
- **Strands Agents SDK**: https://github.com/strands-ai/strands-agents
- **Article**: [Deep Agents Using Strands](http://pierreange.ai/blog/deep-agents-using-strands)
- **Inspiration**: https://github.com/langchain-ai/deepagents

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Built with ❤️ by PA**
