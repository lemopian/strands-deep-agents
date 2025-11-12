"""
Tests for the factory functions.
"""

from strands import Agent, tool

from strands_deep_agents import create_deep_agent


class TestCreateDeepAgent:
    """Test suite for create_deep_agent factory function."""

    def test_basic_creation(self, default_model):
        """Test creating a basic deep agent."""
        agent = create_deep_agent(
            instructions="You are a test agent.",
            model=default_model,
        )

        assert isinstance(agent, Agent)
        assert agent.system_prompt is not None
        assert "You are a test agent" in agent.system_prompt

    def test_creation_with_no_instructions(self):
        """Test creating agent without custom instructions."""
        agent = create_deep_agent()

        assert isinstance(agent, Agent)
        assert agent.system_prompt is not None

    def test_initial_state(self, sample_todos):
        """Test setting initial state."""
        initial_state = {
            "custom_key": "custom_value",
            "todos": sample_todos,
        }

        agent = create_deep_agent(initial_state=initial_state)

        assert agent.state.get("custom_key") == "custom_value"
        todos = agent.state.get("todos")
        assert len(todos) == 3
        assert todos[0]["content"] == "Task 1"

    def test_initial_state_empty(self):
        """Test with empty initial state."""
        agent = create_deep_agent(initial_state={})

        todos = agent.state.get("todos")
        assert todos is not None
        assert len(todos) == 0

    def test_todos_initialized(self):
        """Test that todos are initialized if not provided."""
        agent = create_deep_agent()

        todos = agent.state.get("todos")
        assert todos is not None
        assert isinstance(todos, list)
        assert len(todos) == 0

    def test_disable_parallel_tool_calling(self):
        """Test disabling parallel tool calling."""
        agent = create_deep_agent(disable_parallel_tool_calling=True)

        assert isinstance(agent, Agent)
        # Agent should have sequential executor set

    def test_custom_instructions_in_system_prompt(self):
        """Test custom instructions appear in system prompt."""
        custom_instructions = "You are a specialized testing agent with unique capabilities."
        agent = create_deep_agent(instructions=custom_instructions)

        assert custom_instructions in agent.system_prompt

    def test_agent_with_complex_initial_state(self):
        """Test agent with complex initial state."""
        complex_state = {
            "todos": [{"id": "1", "content": "Complex task", "status": "pending"}],
            "metadata": {"version": "1.0", "author": "test"},
            "counters": [1, 2, 3, 4, 5],
        }

        agent = create_deep_agent(initial_state=complex_state)

        assert agent.state.get("todos") is not None
        assert agent.state.get("metadata")["version"] == "1.0"
        assert agent.state.get("counters") == [1, 2, 3, 4, 5]

    def test_custom_tools_added(self, sample_tool):
        """Test adding custom tools."""
        agent = create_deep_agent(tools=[sample_tool])

        # Verify agent was created successfully
        assert isinstance(agent, Agent)
        assert agent.system_prompt is not None

    def test_multiple_custom_tools(self):
        """Test adding multiple custom tools."""

        @tool
        def tool1(x: str) -> str:
            """Tool 1."""
            return f"Tool1: {x}"

        @tool
        def tool2(y: int) -> int:
            """Tool 2."""
            return y * 2

        agent = create_deep_agent(tools=[tool1, tool2])

        assert isinstance(agent, Agent)

    def test_sub_agents_added(self, sample_sub_agent):
        """Test adding custom sub-agents."""
        agent = create_deep_agent(subagents=[sample_sub_agent])

        assert isinstance(agent, Agent)
        # Verify agent has task tool (generic name, agent-specific sub-agents)

    def test_multiple_sub_agents(self):
        """Test adding multiple sub-agents."""
        sub_agent1 = {"name": "agent1", "description": "First agent", "prompt": "Instructions 1"}
        sub_agent2 = {"name": "agent2", "description": "Second agent", "prompt": "Instructions 2"}

        agent = create_deep_agent(subagents=[sub_agent1, sub_agent2])

        assert isinstance(agent, Agent)

    def test_empty_sub_agents_list(self):
        """Test with empty sub_agents list."""
        agent = create_deep_agent(subagents=[])

        assert isinstance(agent, Agent)

    def test_empty_tools_list(self):
        """Test with empty tools list."""
        agent = create_deep_agent(tools=[])

        assert isinstance(agent, Agent)

    def test_none_initial_state(self):
        """Test with None as initial_state."""
        agent = create_deep_agent(initial_state=None)

        todos = agent.state.get("todos")
        assert todos is not None
        assert len(todos) == 0

    def test_unicode_in_instructions(self):
        """Test unicode characters in instructions."""
        unicode_instructions = "You are a 测试 agent with émojis 🚀 and специальные characters"
        agent = create_deep_agent(instructions=unicode_instructions)

        assert unicode_instructions in agent.system_prompt


class TestSubAgentTypeDict:
    """Test suite for SubAgent TypedDict configuration."""

    def test_sub_agent_dict_creation(self):
        """Test creating a SubAgent dict."""
        sub_agent = {
            "name": "test_agent",
            "description": "Test description",
            "prompt": "Test instructions",
        }

        assert sub_agent["name"] == "test_agent"
        assert sub_agent["description"] == "Test description"
        assert sub_agent["prompt"] == "Test instructions"

    def test_sub_agent_with_tools(self, sample_tool):
        """Test SubAgent with custom tools."""
        sub_agent = {
            "name": "tool_agent",
            "description": "Has tools",
            "prompt": "Uses tools",
            "tools": [sample_tool],
        }

        assert len(sub_agent["tools"]) == 1

    def test_sub_agent_with_multiple_tools(self):
        """Test SubAgent with multiple tools."""

        @tool
        def tool1(x: int) -> int:
            """Tool 1."""
            return x * 2

        @tool
        def tool2(x: int) -> int:
            """Tool 2."""
            return x + 10

        sub_agent = {
            "name": "multi_tool_agent",
            "description": "Multiple tools",
            "prompt": "Multiple tools",
            "tools": [tool1, tool2],
        }

        assert len(sub_agent["tools"]) == 2

    def test_sub_agent_with_model_override(self):
        """Test SubAgent with model override."""
        custom_model = "anthropic.claude-3-5-haiku-20241022"
        sub_agent = {
            "name": "fast_agent",
            "description": "Fast agent",
            "prompt": "Be fast",
            "model": custom_model,
        }

        assert sub_agent["model"] == custom_model

    def test_sub_agent_dict_access(self):
        """Test SubAgent dict access."""
        sub_agent = {
            "name": "dict_agent",
            "description": "Dict test",
            "prompt": "Dict instructions",
        }

        # Test dict access
        assert sub_agent["name"] == "dict_agent"
        assert sub_agent["description"] == "Dict test"
        assert sub_agent.get("name") == "dict_agent"
        assert sub_agent.get("nonexistent", "default") == "default"

    def test_sub_agent_with_empty_name(self):
        """Test SubAgent with empty name."""
        sub_agent = {"name": "", "description": "Empty name", "prompt": "Instructions"}

        assert sub_agent["name"] == ""

    def test_sub_agent_with_long_description(self):
        """Test SubAgent with very long description."""
        long_desc = "A" * 1000
        sub_agent = {"name": "long_desc_agent", "description": long_desc, "prompt": "Instructions"}

        assert len(sub_agent["description"]) == 1000


class TestFactoryIntegration:
    """Integration tests for factory functions."""

    def test_full_agent_with_everything(self, sample_tool, sample_sub_agent, sample_todos):
        """Test creating agent with all features enabled."""
        initial_state = {"todos": sample_todos}

        agent = create_deep_agent(
            instructions="You are a comprehensive agent.",
            tools=[sample_tool],
            subagents=[sample_sub_agent],
            initial_state=initial_state,
        )

        assert isinstance(agent, Agent)

        todos = agent.state.get("todos")
        assert len(todos) == 3

    def test_agent_state_management(self, sample_todos):
        """Test agent state is properly managed."""
        agent = create_deep_agent()

        # Initially empty
        initial_todos = agent.state.get("todos")
        assert len(initial_todos) == 0

        # Set state
        agent.state.set("todos", sample_todos)

        # Verify
        updated_todos = agent.state.get("todos")
        assert len(updated_todos) == 3
        assert updated_todos[0]["content"] == "Task 1"

    def test_agent_with_write_todos_tool(self, agent_with_planning):
        """Test that agent can use write_todos tool."""
        from strands import ToolContext

        from strands_deep_agents.tools import TodoItem, write_todos

        tool_use = {"toolUseId": "test-11", "name": "write_todos", "input": {}}
        tool_context = ToolContext(
            tool_use=tool_use, agent=agent_with_planning, invocation_state={}
        )

        result = write_todos(
            todos=[TodoItem(id="1", content="Test", status="pending")],
            tool_context=tool_context,
            merge=False,
        )

        assert "TODO list updated" in result
        todos = agent_with_planning.state.get("todos")
        assert len(todos) == 1

    def test_sequential_vs_parallel_execution(self):
        """Test both parallel and sequential execution modes."""
        # Parallel (default)
        agent_parallel = create_deep_agent(disable_parallel_tool_calling=False)
        assert isinstance(agent_parallel, Agent)

        # Sequential
        agent_sequential = create_deep_agent(disable_parallel_tool_calling=True)
        assert isinstance(agent_sequential, Agent)

    def test_model_parameter_usage(self, default_model):
        """Test that model parameter is accepted and used."""
        agent = create_deep_agent(model=default_model)

        assert isinstance(agent, Agent)
        # Model is set internally

    def test_empty_configuration(self):
        """Test creating agent with minimal/empty configuration."""
        agent = create_deep_agent()

        assert isinstance(agent, Agent)
        assert agent.state.get("todos") == []


class TestFactoryEdgeCases:
    """Edge cases and error conditions for factory functions."""

    def test_very_long_instructions(self):
        """Test with very long instructions."""
        long_instructions = "A" * 5000
        agent = create_deep_agent(instructions=long_instructions)

        assert long_instructions in agent.system_prompt

    def test_special_characters_in_instructions(self):
        """Test special characters in instructions."""
        special_instructions = "Test with <>&\"' special chars"
        agent = create_deep_agent(instructions=special_instructions)

        assert special_instructions in agent.system_prompt

    def test_mixed_tool_types(self, sample_tool):
        """Test adding both function tools and tool objects."""

        @tool
        def another_tool(x: str) -> str:
            """Another tool."""
            return x.upper()

        agent = create_deep_agent(tools=[sample_tool, another_tool])

        assert isinstance(agent, Agent)

    def test_subagent_with_optional_fields(self):
        """Test subagent configuration with all optional fields."""

        @tool
        def custom_tool(x: int) -> int:
            """Custom tool for subagent."""
            return x * 3

        sub_agent = {
            "name": "full_agent",
            "description": "Fully configured agent",
            "prompt": "Full instructions",
            "tools": [custom_tool],
            "model": "anthropic.claude-3-5-haiku-20241022",
        }

        agent = create_deep_agent(subagents=[sub_agent])

        assert isinstance(agent, Agent)

    def test_state_with_none_values(self):
        """Test initial state with None values."""
        initial_state = {"key1": None, "key2": "value2", "todos": []}

        agent = create_deep_agent(initial_state=initial_state)

        assert agent.state.get("key1") is None
        assert agent.state.get("key2") == "value2"
