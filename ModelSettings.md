Help on class ModelSettings in module agents.model_settings:

class ModelSettings(builtins.object)
 |  ModelSettings(
 |      temperature: 'float | None' = None,
 |      top_p: 'float | None' = None,
 |      frequency_penalty: 'float | None' = None,
 |      presence_penalty: 'float | None' = None,
 |      tool_choice: 'ToolChoice | None' = None,
 |      parallel_tool_calls: 'bool | None' = None,
 |      truncation: "Literal['auto', 'disabled'] | None" = None,
 |      max_tokens: 'int | None' = None,
 |      reasoning: 'Reasoning | None' = None,
 |      verbosity: "Literal['low', 'medium', 'high'] | None" = None,
 |      metadata: 'dict[str, str] | None' = None,
 |      store: 'bool | None' = None,
 |      prompt_cache_retention: "Literal['in_memory', '24h'] | None" = None,
 |      include_usage: 'bool | None' = None,
 |      response_include: 'list[ResponseIncludable | str] | None' = None,
 |      top_logprobs: 'int | None' = None,
 |      extra_query: 'Query | None' = None,
 |      extra_body: 'Body | None' = None,
 |      extra_headers: 'Headers | None' = None,
 |      extra_args: 'dict[str, Any] | None' = None
 |  ) -> None
 |
 |  Settings to use when calling an LLM.
 |
 |  This class holds optional model configuration parameters (e.g. temperature,
 |  top_p, penalties, truncation, etc.).
 |
 |  Not all models/providers support all of these parameters, so please check the API documentation
 |  for the specific model and provider you are using.
 |
 |  Methods defined here:
 |
 |  __eq__(self, other)
 |      Return self==value.
 |
 |  __init__(__dataclass_self__: 'PydanticDataclass', *args: 'Any', **kwargs: 'Any') -> 'None' from pydantic._internal._dataclasses.ModelSettings
 |      # dataclass.__init__ must be defined here so its `__qualname__` can be changed since functions can't be copied,
 |      # and so that the mock validator is used if building was deferred:
 |
 |  __replace__ = _replace(self, /, **changes) from dataclasses
 |
 |  __repr__(self)
 |      Return repr(self).
 |
 |  resolve(self, override: 'ModelSettings | None') -> 'ModelSettings'
 |      Produce a new ModelSettings by overlaying any non-None values from the
 |      override on top of this instance.
 |
 |  to_json_dict(self) -> 'dict[str, Any]'
 |
 |  ----------------------------------------------------------------------
 |  Class methods defined here:
 |
 |  __pydantic_fields_complete__ = _pydantic_fields_complete() -> 'bool' from pydantic.dataclasses
 |      Return whether the fields where successfully collected (i.e. type hints were successfully resolves).
 |
 |      This is a private property, not meant to be used outside Pydantic.
 |
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |
 |  __dict__
 |      dictionary for instance variables
 |
 |  __weakref__
 |      list of weak references to the object
 |
 |  ----------------------------------------------------------------------
 |  Data and other attributes defined here:
 |
 |  __annotations__ = {'extra_args': 'dict[str, Any] | None', 'extra_body'...
 |
 |  __dataclass_fields__ = {'extra_args': Field(name='extra_args',type='di...
 |
 |  __dataclass_params__ = _DataclassParams(init=True,repr=True,eq=True,or...
 |
 |  __hash__ = None
 |
 |  __is_pydantic_dataclass__ = True
 |
 |  __match_args__ = ('temperature', 'top_p', 'frequency_penalty', 'presen...
 |
 |  __pydantic_complete__ = True
 |
 |  __pydantic_config__ = {}
 |
 |  __pydantic_core_schema__ = {'cls': <class 'agents.model_settings.Model...
 |
 |  __pydantic_decorators__ = DecoratorInfos(validators={}, field_validato...
 |
 |  __pydantic_fields__ = {'extra_args': FieldInfo(annotation=Union[dict[s...
 |
 |  __pydantic_serializer__ = SchemaSerializer(serializer=Dataclass(
 |      D...
 |
 |  __pydantic_validator__ = SchemaValidator(title="ModelSettings", valida...
 |
 |  __signature__ = <Signature (temperature: 'float | None' = None, ...ra_...
 |
 |  extra_args = None
 |
 |  extra_body = None
 |
 |  extra_headers = None
 |
 |  extra_query = None
 |
 |  frequency_penalty = None
 |
 |  include_usage = None
 |
 |  max_tokens = None
 |
 |  metadata = None
 |
 |  parallel_tool_calls = None
 |
 |  presence_penalty = None
 |
 |  prompt_cache_retention = None
 |
 |  reasoning = None
 |
 |  response_include = None
 |
 |  store = None
 |
 |  temperature = None
 |
 |  tool_choice = None
 |
 |  top_logprobs = None
 |
 |  top_p = None
 |
 |  truncation = None
 |
 |  verbosity = None

