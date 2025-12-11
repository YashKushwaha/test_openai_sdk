Help on class Agent in module agents.agent:

class Agent(AgentBase, typing.Generic)
 |  Agent(
 |      name: 'str',
 |      handoff_description: 'str | None' = None,
 |      tools: 'list[Tool]' = <factory>,
 |      mcp_servers: 'list[MCPServer]' = <factory>,
 |      mcp_config: 'MCPConfig' = <factory>,
 |      instructions: 'str | Callable[[RunContextWrapper[TContext], Agent[TContext]], MaybeAwaitable[str]] | None' = None,
 |      prompt: 'Prompt | DynamicPromptFunction | None' = None,
 |      handoffs: 'list[Agent[Any] | Handoff[TContext, Any]]' = <factory>,
 |      model: 'str | Model | None' = None,
 |      model_settings: 'ModelSettings' = <factory>,
 |      input_guardrails: 'list[InputGuardrail[TContext]]' = <factory>,
 |      output_guardrails: 'list[OutputGuardrail[TContext]]' = <factory>,
 |      output_type: 'type[Any] | AgentOutputSchemaBase | None' = None,
 |      hooks: 'AgentHooks[TContext] | None' = None,
 |      tool_use_behavior: "Literal['run_llm_again', 'stop_on_first_tool'] | StopAtTools | ToolsToFinalOutputFunction" = 'run_llm_again',
 |      reset_tool_choice: 'bool' = True
 |  ) -> None
 |
 |  An agent is an AI model configured with instructions, tools, guardrails, handoffs and more.
 |
 |  We strongly recommend passing `instructions`, which is the "system prompt" for the agent. In
 |  addition, you can pass `handoff_description`, which is a human-readable description of the
 |  agent, used when the agent is used inside tools/handoffs.
 |
 |  Agents are generic on the context type. The context is a (mutable) object you create. It is
 |  passed to tool functions, handoffs, guardrails, etc.
 |
 |  See `AgentBase` for base parameters that are shared with `RealtimeAgent`s.
 |
 |  Method resolution order:
 |      Agent
 |      AgentBase
 |      typing.Generic
 |      builtins.object
 |
 |  Methods defined here:
 |
 |  __eq__(self, other)
 |      Return self==value.
 |
 |  __init__(
 |      self,
 |      name: 'str',
 |      handoff_description: 'str | None' = None,
 |      tools: 'list[Tool]' = <factory>,
 |      mcp_servers: 'list[MCPServer]' = <factory>,
 |      mcp_config: 'MCPConfig' = <factory>,
 |      instructions: 'str | Callable[[RunContextWrapper[TContext], Agent[TContext]], MaybeAwaitable[str]] | None' = None,
 |      prompt: 'Prompt | DynamicPromptFunction | None' = None,
 |      handoffs: 'list[Agent[Any] | Handoff[TContext, Any]]' = <factory>,
 |      model: 'str | Model | None' = None,
 |      model_settings: 'ModelSettings' = <factory>,
 |      input_guardrails: 'list[InputGuardrail[TContext]]' = <factory>,
 |      output_guardrails: 'list[OutputGuardrail[TContext]]' = <factory>,
 |      output_type: 'type[Any] | AgentOutputSchemaBase | None' = None,
 |      hooks: 'AgentHooks[TContext] | None' = None,
 |      tool_use_behavior: "Literal['run_llm_again', 'stop_on_first_tool'] | StopAtTools | ToolsToFinalOutputFunction" = 'run_llm_again',
 |      reset_tool_choice: 'bool' = True
 |  ) -> None
 |      Initialize self.  See help(type(self)) for accurate signature.
 |
 |  __post_init__(self)
 |
 |  __replace__ = _replace(self, /, **changes) from dataclasses
 |
 |  __repr__(self)
 |      Return repr(self).
 |
 |  as_tool(
 |      self,
 |      tool_name: 'str | None',
 |      tool_description: 'str | None',
 |      custom_output_extractor: 'Callable[[RunResult], Awaitable[str]] | None' = None,
 |      is_enabled: 'bool | Callable[[RunContextWrapper[Any], AgentBase[Any]], MaybeAwaitable[bool]]' = True,
 |      run_config: 'RunConfig | None' = None,
 |      max_turns: 'int | None' = None,
 |      hooks: 'RunHooks[TContext] | None' = None,
 |      previous_response_id: 'str | None' = None,
 |      conversation_id: 'str | None' = None,
 |      session: 'Session | None' = None
 |  ) -> 'Tool'
 |      Transform this agent into a tool, callable by other agents.
 |
 |      This is different from handoffs in two ways:
 |      1. In handoffs, the new agent receives the conversation history. In this tool, the new agent
 |         receives generated input.
 |      2. In handoffs, the new agent takes over the conversation. In this tool, the new agent is
 |         called as a tool, and the conversation is continued by the original agent.
 |
 |      Args:
 |          tool_name: The name of the tool. If not provided, the agent's name will be used.
 |          tool_description: The description of the tool, which should indicate what it does and
 |              when to use it.
 |          custom_output_extractor: A function that extracts the output from the agent. If not
 |              provided, the last message from the agent will be used.
 |          is_enabled: Whether the tool is enabled. Can be a bool or a callable that takes the run
 |              context and agent and returns whether the tool is enabled. Disabled tools are hidden
 |              from the LLM at runtime.
 |
 |  clone(self, **kwargs: 'Any') -> 'Agent[TContext]'
 |      Make a copy of the agent, with the given arguments changed.
 |      Notes:
 |          - Uses `dataclasses.replace`, which performs a **shallow copy**.
 |          - Mutable attributes like `tools` and `handoffs` are shallow-copied:
 |            new list objects are created only if overridden, but their contents
 |            (tool functions and handoff objects) are shared with the original.
 |          - To modify these independently, pass new lists when calling `clone()`.
 |      Example:
 |          ```python
 |          new_agent = agent.clone(instructions="New instructions")
 |          ```
 |
 |  async get_prompt(self, run_context: 'RunContextWrapper[TContext]') -> 'ResponsePromptParam | None'
 |      Get the prompt for the agent.
 |
 |  async get_system_prompt(self, run_context: 'RunContextWrapper[TContext]') -> 'str | None'
 |
 |  ----------------------------------------------------------------------
 |  Data and other attributes defined here:
 |
 |  __annotations__ = {'handoffs': 'list[Agent[Any] | Handoff[TContext, An...
 |
 |  __dataclass_fields__ = {'handoff_description': Field(name='handoff_des...
 |
 |  __dataclass_params__ = _DataclassParams(init=True,repr=True,eq=True,or...
 |
 |  __hash__ = None
 |
 |  __match_args__ = ('name', 'handoff_description', 'tools', 'mcp_servers...
 |
 |  __orig_bases__ = (<class 'agents.agent.AgentBase'>, typing.Generic[~TC...
 |
 |  __parameters__ = (~TContext,)
 |
 |  hooks = None
 |
 |  instructions = None
 |
 |  model = None
 |
 |  output_type = None
 |
 |  prompt = None
 |
 |  reset_tool_choice = True
 |
 |  tool_use_behavior = 'run_llm_again'
 |
 |  ----------------------------------------------------------------------
 |  Methods inherited from AgentBase:
 |
 |  async get_all_tools(self, run_context: 'RunContextWrapper[TContext]') -> 'list[Tool]'
 |      All agent tools, including MCP tools and function tools.
 |
 |  async get_mcp_tools(self, run_context: 'RunContextWrapper[TContext]') -> 'list[Tool]'
 |      Fetches the available tools from the MCP servers.
 |
 |  ----------------------------------------------------------------------
 |  Data descriptors inherited from AgentBase:
 |
 |  __dict__
 |      dictionary for instance variables
 |
 |  __weakref__
 |      list of weak references to the object
 |
 |  ----------------------------------------------------------------------
 |  Data and other attributes inherited from AgentBase:
 |
 |  handoff_description = None
 |
 |  ----------------------------------------------------------------------
 |  Class methods inherited from typing.Generic:
 |
 |  __class_getitem__(...)
 |      Parameterizes a generic class.
 |
 |      At least, parameterizing a generic class is the *main* thing this
 |      method does. For example, for some generic class `Foo`, this is called
 |      when we do `Foo[int]` - there, with `cls=Foo` and `params=int`.
 |
 |      However, note that this method is also called when defining generic
 |      classes in the first place with `class Foo[T]: ...`.
 |
 |  __init_subclass__(...)
 |      Function to initialize subclasses.

