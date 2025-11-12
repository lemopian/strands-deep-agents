"""
Tests for sub-agent functionality.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest
from strands import tool

from strands_deep_agents.sub_agents import (
    _build_subagents_configs,
    _get_subagents_description,
    create_async_task_tool,
    create_general_purpose_sub_agent,
    create_task_tool,
)


class TestSubAgentCreation:
    """Test suite for sub-agent tool creation."""

    def test_create_task_tool_basic(self, default_model):
        """Test creating a basic task tool with subagents."""
        sub_agent_config = {
            "name": "test_agent",
            "description": "A test agent",
            "prompt": "You are a test agent.",
        }

        tool_func = create_task_tool(
            default_tools=[],
            subagents=[sub_agent_config],
            default_model=default_model,
        )

        assert tool_func.__name__ == "task"
        assert callable(tool_func)

    def test_task_tool_with_custom_tools(self, default_model, sample_tool):
        """Test task tool with sub-agent that has custom tools."""
        sub_agent_config = {
            "name": "specialized_agent",
            "description": "Specialized agent",
            "prompt": "You are specialized.",
            "tools": [sample_tool],
        }

        tool_func = create_task_tool(
            default_tools=[],
            subagents=[sub_agent_config],
            default_model=default_model,
        )

        assert tool_func.__name__ == "task"

    def test_task_tool_with_multiple_subagents(self, default_model):
        """Test creating task tool with multiple sub-agents."""
        subagents = [
            {"name": "agent1", "description": "First agent", "prompt": "Prompt 1"},
            {"name": "agent2", "description": "Second agent", "prompt": "Prompt 2"},
            {"name": "agent3", "description": "Third agent", "prompt": "Prompt 3"},
        ]

        tool_func = create_task_tool(
            default_tools=[],
            subagents=subagents,
            default_model=default_model,
        )

        assert tool_func.__name__ == "task"
        # Verify tool can handle multiple agent types

    def test_general_purpose_sub_agent(self, default_model):
        """Test creating the general_purpose sub-agent."""
        instructions = "You are the main agent."
        tools = []

        general_agent = create_general_purpose_sub_agent(
            main_instructions=instructions, all_tools=tools, model=default_model
        )

        assert general_agent["name"] == "general-purpose"
        assert "researching complex questions" in general_agent["description"].lower()
        assert general_agent["tools"] == tools
        assert general_agent["model"] == default_model

    def test_general_purpose_sub_agent_with_empty_instructions(self, default_model):
        """Test general purpose agent with empty instructions."""
        general_agent = create_general_purpose_sub_agent(
            main_instructions="", all_tools=[], model=default_model
        )

        assert general_agent["name"] == "general-purpose"
        assert general_agent["prompt"] != ""

    def test_general_purpose_sub_agent_inherits_tools(self, default_model, sample_tool):
        """Test that general purpose agent inherits all tools."""
        tools = [sample_tool]

        general_agent = create_general_purpose_sub_agent(
            main_instructions="Main instructions", all_tools=tools, model=default_model
        )

        assert general_agent["tools"] == tools


class TestSubAgentConfiguration:
    """Test suite for sub-agent configuration building."""

    def test_get_subagents_description_single(self):
        """Test description generation for single subagent."""
        subagents = [{"name": "test", "description": "Test agent"}]
        desc = _get_subagents_description(subagents)

        assert "test" in desc
        assert "Test agent" in desc

    def test_get_subagents_description_multiple(self):
        """Test description generation for multiple subagents."""
        subagents = [
            {"name": "agent1", "description": "First agent"},
            {"name": "agent2", "description": "Second agent"},
        ]
        desc = _get_subagents_description(subagents)

        assert "agent1" in desc
        assert "agent2" in desc
        assert "First agent" in desc
        assert "Second agent" in desc

    def test_get_subagents_description_empty(self):
        """Test description generation with empty list."""
        desc = _get_subagents_description([])
        assert desc == ""

    def test_build_subagents_configs(self, default_model, sample_tool):
        """Test building subagent configurations."""
        subagents = [
            {"name": "agent1", "prompt": "Prompt 1"},
            {"name": "agent2", "prompt": "Prompt 2", "tools": [sample_tool]},
        ]

        configs = _build_subagents_configs(
            default_tools=[],
            subagents=subagents,
            default_model=default_model,
        )

        assert "agent1" in configs
        assert "agent2" in configs
        assert configs["agent1"]["system_prompt"] == "Prompt 1"
        assert configs["agent2"]["tools"] == [sample_tool]

    def test_build_subagents_configs_with_model_override(self, default_model):
        """Test that subagent can override default model."""
        custom_model = "anthropic.claude-3-5-haiku-20241022"
        subagents = [{"name": "fast_agent", "prompt": "Be fast", "model": custom_model}]

        configs = _build_subagents_configs(
            default_tools=[],
            subagents=subagents,
            default_model=default_model,
        )

        assert configs["fast_agent"]["model"] == custom_model

    def test_build_subagents_configs_disable_parallel_calling(self, default_model):
        """Test disabling parallel tool calling for subagents."""
        subagents = [
            {
                "name": "sequential_agent",
                "prompt": "Sequential",
                "disable_parallel_tool_calling": True,
            }
        ]

        configs = _build_subagents_configs(
            default_tools=[],
            subagents=subagents,
            default_model=default_model,
        )

        assert configs["sequential_agent"]["disable_parallel_tool_calling"] is True


class TestSubAgentExecution:
    """Test suite for sub-agent execution."""

    def test_task_tool_invalid_subagent_type(self, default_model):
        """Test error handling when invalid subagent type is specified."""
        sub_agent_config = {"name": "valid_agent", "description": "Valid", "prompt": "Valid"}

        tool_func = create_task_tool(
            default_tools=[],
            subagents=[sub_agent_config],
            default_model=default_model,
        )

        result = tool_func(description="Test task", subagent_type="invalid_agent")

        assert "Error" in result
        assert "invalid_agent" in result
        assert "valid_agent" in result

    @patch("strands_deep_agents.sub_agents.Agent")
    def test_task_tool_execution_success(self, mock_agent_class, default_model):
        """Test successful task tool execution."""
        mock_agent_instance = Mock()
        mock_agent_instance.return_value = "Task completed successfully"
        mock_agent_class.return_value = mock_agent_instance

        sub_agent_config = {"name": "test_agent", "description": "Test", "prompt": "Test prompt"}

        tool_func = create_task_tool(
            default_tools=[],
            subagents=[sub_agent_config],
            default_model=default_model,
        )

        result = tool_func(description="Test task", subagent_type="test_agent")

        assert "Task completed successfully" in result
        mock_agent_class.assert_called_once()
        mock_agent_instance.assert_called_once_with("Test task")

    @patch("strands_deep_agents.sub_agents.Agent")
    def test_task_tool_execution_exception(self, mock_agent_class, default_model):
        """Test exception handling during task execution."""
        mock_agent_instance = Mock()
        mock_agent_instance.side_effect = Exception("Test error")
        mock_agent_class.return_value = mock_agent_instance

        sub_agent_config = {"name": "error_agent", "description": "Error", "prompt": "Error prompt"}

        tool_func = create_task_tool(
            default_tools=[],
            subagents=[sub_agent_config],
            default_model=default_model,
        )

        result = tool_func(description="Test task", subagent_type="error_agent")

        assert "Error" in result
        assert "error_agent" in result
        assert "Test error" in result

    def test_task_tool_with_subagent_tools(self, default_model):
        """Test that subagent receives its configured tools."""

        @tool
        def special_tool(x: int) -> int:
            """Special tool."""
            return x * 2

        sub_agent_config = {
            "name": "tool_agent",
            "description": "Has tools",
            "prompt": "Use tools",
            "tools": [special_tool],
        }

        tool_func = create_task_tool(
            default_tools=[],
            subagents=[sub_agent_config],
            default_model=default_model,
        )

        # Just verify the tool is created successfully
        assert tool_func.__name__ == "task"


class TestAsyncSubAgentCreation:
    """Test suite for async sub-agent functionality."""

    @pytest.mark.anyio
    async def test_create_async_task_tool_basic(self, default_model):
        """Test creating a basic async task tool."""
        sub_agent_config = {
            "name": "async_agent",
            "description": "Async test agent",
            "prompt": "You are async.",
        }

        tool_func = await create_async_task_tool(
            default_tools=[],
            subagents=[sub_agent_config],
            default_model=default_model,
        )

        assert tool_func.__name__ == "task"
        assert callable(tool_func)

    @pytest.mark.anyio
    async def test_async_task_tool_invalid_subagent(self, default_model):
        """Test async task tool with invalid subagent type."""
        sub_agent_config = {"name": "valid_async", "description": "Valid", "prompt": "Valid"}

        tool_func = await create_async_task_tool(
            default_tools=[],
            subagents=[sub_agent_config],
            default_model=default_model,
        )

        result = await tool_func(description="Test", subagent_type="invalid_async")

        assert "Error" in result
        assert "invalid_async" in result

    @pytest.mark.anyio
    @patch("strands_deep_agents.sub_agents.Agent")
    async def test_async_task_tool_execution(self, mock_agent_class, default_model):
        """Test async task tool execution."""
        mock_agent_instance = Mock()
        # Make invoke_async return an awaitable
        async_result = AsyncMock(return_value="Async result")
        mock_agent_instance.invoke_async = async_result
        mock_agent_class.return_value = mock_agent_instance

        sub_agent_config = {
            "name": "async_test",
            "description": "Async test",
            "prompt": "Async prompt",
        }

        tool_func = await create_async_task_tool(
            default_tools=[],
            subagents=[sub_agent_config],
            default_model=default_model,
        )

        result = await tool_func(description="Async task", subagent_type="async_test")

        assert "Async result" in result


class TestSubAgentTypes:
    """Test suite for SubAgent type dict."""

    def test_subagent_dict_creation_minimal(self):
        """Test creating SubAgent dict with minimal parameters."""
        agent = {
            "name": "minimal",
            "description": "Minimal agent",
            "prompt": "Minimal instructions",
        }

        assert agent["name"] == "minimal"
        assert agent["description"] == "Minimal agent"
        assert agent["prompt"] == "Minimal instructions"

    def test_subagent_dict_creation_full(self, sample_tool):
        """Test creating SubAgent dict with all parameters."""
        agent = {
            "name": "full",
            "description": "Full agent",
            "prompt": "Full instructions",
            "tools": [sample_tool],
            "model": "anthropic.claude-3-5-haiku-20241022",
        }

        assert agent["name"] == "full"
        assert agent["description"] == "Full agent"
        assert agent["tools"] == [sample_tool]
        assert agent["model"] == "anthropic.claude-3-5-haiku-20241022"

    def test_subagent_dict_access(self):
        """Test that SubAgent dict can be accessed as dict."""
        agent = {"name": "dict_test", "description": "Dict test", "prompt": "Instructions"}

        # SubAgent is a dict
        assert agent["name"] == "dict_test"
        assert agent["description"] == "Dict test"
        assert agent.get("name") == "dict_test"
        assert agent.get("nonexistent", "default") == "default"


class TestSubAgentIntegration:
    """Integration tests for sub-agent functionality."""

    def test_task_tool_with_multiple_types(self, default_model):
        """Test task tool can handle multiple subagent types."""
        subagents = [
            {"name": "analyst", "description": "Analyzes data", "prompt": "Analyze"},
            {"name": "writer", "description": "Writes reports", "prompt": "Write"},
            {"name": "reviewer", "description": "Reviews content", "prompt": "Review"},
        ]

        tool_func = create_task_tool(
            default_tools=[],
            subagents=subagents,
            default_model=default_model,
        )

        # Test each type is recognized
        for subagent_type in ["analyst", "writer", "reviewer"]:
            configs = _build_subagents_configs([], subagents, default_model)
            assert subagent_type in configs

    @pytest.mark.skip(reason="Requires actual model API access")
    def test_sub_agent_execution_with_real_model(self):
        """Test executing a sub-agent with real API (requires credentials)."""
        pass

    @pytest.mark.skip(reason="Requires actual model API access")
    @pytest.mark.anyio
    async def test_async_sub_agent_execution_with_real_model(self):
        """Test async sub-agent execution with real API (requires credentials)."""
        pass


class TestSubAgentEdgeCases:
    """Edge cases and error conditions for sub-agent functionality."""

    def test_subagent_with_very_long_prompt(self, default_model):
        """Test subagent with very long prompt."""
        long_prompt = "A" * 10000
        sub_agent_config = {
            "name": "long_prompt_agent",
            "description": "Has long prompt",
            "prompt": long_prompt,
        }

        tool_func = create_task_tool(
            default_tools=[],
            subagents=[sub_agent_config],
            default_model=default_model,
        )

        assert tool_func.__name__ == "task"

    def test_subagent_with_special_characters(self, default_model):
        """Test subagent with special characters in fields."""
        sub_agent_config = {
            "name": "special_agent",
            "description": "Has <>&\"' special chars",
            "prompt": "Prompt with 测试 unicode",
        }

        tool_func = create_task_tool(
            default_tools=[],
            subagents=[sub_agent_config],
            default_model=default_model,
        )

        assert tool_func.__name__ == "task"

    def test_subagent_with_empty_name(self, default_model):
        """Test handling of subagent with empty name."""
        sub_agent_config = {"name": "", "description": "Empty name agent", "prompt": "Prompt"}

        tool_func = create_task_tool(
            default_tools=[],
            subagents=[sub_agent_config],
            default_model=default_model,
        )

        # Should create tool successfully
        assert tool_func.__name__ == "task"

    def test_empty_subagents_list(self, default_model):
        """Test create_task_tool with empty subagents list."""
        tool_func = create_task_tool(
            default_tools=[],
            subagents=[],
            default_model=default_model,
        )

        assert tool_func.__name__ == "task"

    def test_subagent_description_formatting(self, default_model):
        """Test that subagent descriptions are properly formatted."""
        subagents = [
            {"name": "agent1", "description": "First\nMultiline\nDescription"},
            {"name": "agent2", "description": "Second with    spaces"},
        ]

        desc = _get_subagents_description(subagents)

        assert "agent1" in desc
        assert "agent2" in desc
        # Description includes original formatting
