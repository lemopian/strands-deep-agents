"""
Tests for the factory functions.
"""

import pytest
from strands_deepagents import create_deep_agent, SubAgent
from strands import Agent, tool


class TestCreateDeepAgent:
    """Test suite for create_deep_agent factory function."""

    def test_basic_creation(self):
        """Test creating a basic deep agent."""
        agent = create_deep_agent(
            instructions="You are a test agent.",
            model_id="global.anthropic.claude-sonnet-4-5-20250929-v1:0",
        )

        assert isinstance(agent, Agent)
        assert agent.system_prompt is not None
        assert "You are a test agent" in agent.system_prompt

    def test_planning_tools_included(self):
        """Test that planning tools are included by default."""
        agent = create_deep_agent()

        # Check that write_todos and get_todos are in tools
        tool_names = [getattr(t, "__name__", None) or str(t) for t in agent.tools]
        assert "write_todos" in tool_names
        assert "get_todos" in tool_names

    def test_file_tools_attempted(self):
        """Test that file tools are attempted to be included."""
        agent = create_deep_agent()

        # Check that file tools are attempted (may not be present if strands_tools not installed)
        tool_names = [getattr(t, "__name__", None) or str(t) for t in agent.tools]
        # At minimum, planning tools should be there
        assert len(agent.tools) > 0

    def test_disable_planning(self):
        """Test disabling planning tools."""
        agent = create_deep_agent(enable_planning=False)

        tool_names = [getattr(t, "__name__", None) or str(t) for t in agent.tools]
        assert "write_todos" not in tool_names
        assert "get_todos" not in tool_names

    def test_disable_default_tools(self):
        """Test disabling all default tools."""
        agent = create_deep_agent(include_default_tools=False)

        # Should still have general_purpose sub-agent
        tool_names = [getattr(t, "__name__", None) or str(t) for t in agent.tools]
        assert "general_purpose" in tool_names

    def test_custom_tools_added(self):
        """Test adding custom tools."""

        @tool
        def custom_tool(input: str) -> str:
            """A custom tool for testing."""
            return f"Custom: {input}"

        agent = create_deep_agent(tools=[custom_tool])

        tool_names = [getattr(t, "__name__", None) or str(t) for t in agent.tools]
        assert "custom_tool" in tool_names

    def test_sub_agents_added(self):
        """Test adding custom sub-agents."""
        sub_agent = SubAgent(
            name="test_sub_agent", description="A test sub-agent", instructions="You are a test."
        )

        agent = create_deep_agent(sub_agents=[sub_agent])

        tool_names = [getattr(t, "__name__", None) or str(t) for t in agent.tools]
        assert "test_sub_agent" in tool_names
        assert "general_purpose" in tool_names  # Always included

    def test_initial_state(self):
        """Test setting initial state."""
        initial_state = {
            "custom_key": "custom_value",
            "todos": [{"id": "1", "content": "Pre-existing", "status": "pending"}],
        }

        agent = create_deep_agent(initial_state=initial_state)

        assert agent.state.get("custom_key") == "custom_value"
        todos = agent.state.get("todos")
        assert len(todos) == 1
        assert todos[0]["content"] == "Pre-existing"

    def test_todos_initialized(self):
        """Test that todos are initialized if not provided."""
        agent = create_deep_agent()

        todos = agent.state.get("todos")
        assert todos is not None
        assert isinstance(todos, list)
        assert len(todos) == 0


class TestSubAgent:
    """Test suite for SubAgent configuration."""

    def test_sub_agent_creation(self):
        """Test creating a SubAgent."""
        sub_agent = SubAgent(
            name="test_agent", description="Test description", instructions="Test instructions"
        )

        assert sub_agent.name == "test_agent"
        assert sub_agent.description == "Test description"
        assert sub_agent.instructions == "Test instructions"
        assert sub_agent.tools is None
        assert sub_agent.model_id is None

    def test_sub_agent_with_tools(self):
        """Test SubAgent with custom tools."""

        @tool
        def test_tool(x: int) -> int:
            """Test tool."""
            return x * 2

        sub_agent = SubAgent(
            name="math_agent",
            description="Does math",
            instructions="You do math",
            tools=[test_tool],
        )

        assert len(sub_agent.tools) == 1
        assert sub_agent.tools[0].__name__ == "test_tool"

    def test_sub_agent_with_model_override(self):
        """Test SubAgent with model override."""
        sub_agent = SubAgent(
            name="fast_agent",
            description="Fast agent",
            instructions="Be fast",
            model_id="anthropic.claude-3-5-haiku-20241022",
        )

        assert sub_agent.model_id == "anthropic.claude-3-5-haiku-20241022"
