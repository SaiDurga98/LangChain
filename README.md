# You can find the code in the master branch
# This repository contains the notes on how we can use LangChain Framework to build applications leveraging LLMs.

1. What is langchain ?

 LangChain is an open-source framework for developing applications powered by large language models (LLMs).

2. Why I'm learning it ?

a) It’s model-agnostic,  means the code or framework isn’t tied to one specific AI model or vendor. You can swap models (OpenAI, Anthropic, local Llama, Hugging Face models, etc.) without rewriting your app logic—just change the model plug-in/config.

b) It provides complete ecosystem like the concept of chains, memory and state handling.

3. How I plan to use it like what can we build with it?

a) Conversational Chatbots

b) AI knowledge Assistants

c) AI Agents ( the boom that's going on now)

d) Workflow Automation

e) Summarization/Research Helpers

4. Core ideas I’m starting with :

a) **LangChain components (Models, Prompts, Chains, Memory, Indexes, Agents)**

 • **Models** – In LangChain, “models” are the core interfaces through which you interact with AI models. They do Natural Language Understanding and Context aware text generation brains.

LLMs: classic “text in → text out” (good for single prompts).

Chat models: Built for conversations (handle roles like system/user/assistant, play nicely with history and tool calls).

Embeddings : turn text into vectors so you can search by meaning(semantic search).

 • **Prompts** – The instructions you give the model to guide the output

Write them as templates with variables so they’re reusable and consistent.
For chat, use chat prompts with roles (system/human/ai) and drop in past messages(using MessagePlaceHolders) when you need memory.
1. Dynamic and reusable prompts
2. Role based prompts
3. Few shot prompting

Prompt building blocks in LangChain
1) PromptTemplate (single text)
Builds one string from a template and variables.
Best for single-turn tasks.
2)ChatPromptTemplate (list of messages)
Builds a sequence of messages (system/human/ai/…).
Best for chat, multi-turn, tool use, and role control.
3) Messages & MessagePlaceholder
Message types:
SystemMessage – sets behavior/instructions.
HumanMessage – user input.
AIMessage – model’s prior reply (if you’re replaying history).
Tool/Function/ToolMessage – tool-calling traces (agents).
MessagesPlaceholder: Injects a list of messages (e.g., conversation history) into a chat template at runtime.

Model.invoke(...)
├─ Single text (single-turn)
│  ├─ Static: "literal string"
│  └─ Dynamic: PromptTemplate → str
│
└─ List of messages (chat / multi-turn)
   ├─ Static: [SystemMessage, HumanMessage, ...]
   └─ Dynamic: ChatPromptTemplate (+ MessagesPlaceholder)

   • **Structured Outputs** : In LangChain, structured output means making the model return data in a well-defined format (e.g., JSON) instead of free-form text, so your app can parse and use it programmatically.
1) Why do we need it?
Common scenarios where structure matters:
Data extraction
API building
Agents (tool use / automation needs predictable fields)

2) Ways to get structured output
A) “Prompt it out” (instruct the model to return JSON)
Write a clear instruction and a small schema in your prompt:
“Return the response in JSON with fields X, Y, Z.”

B) with_structured_output(...)
LangChain exposes a helper (shown as **with_structured_output**) that binds a schema to your model so responses are coerced into that structure. Use it with a TypedDict or a Pydantic model.

**TypedDict**: declares required keys & value types (type hints), but does not do runtime validation by itself.
**Pydantic**: adds data parsing & validation, defaults, descriptions, optionals, coercion, regex, constraints, and can output .json()/.dict().
In Pydantic, Field(...) is how you add defaults, validation rules, and metadata to a model attribute. It powers both runtime validation and the generated JSON Schema (great for LangChain structured outputs).
What Field is for?
  Default values
  Field(default=...) or default_factory=... (for dynamic defaults)
Validation constraints
  Numbers: gt, ge, lt, le, multiple_of
  Strings/bytes: min_length, max_length, pattern (regex)
  Arrays: min_items, max_items, unique_items
  Schema & docs metadata
  title, description, examples, deprecated, json_schema_extra
Aliasing & I/O control (v2)
  validation_alias, serialization_alias, alias (legacy)
  repr, exclude, frozen, validate_default
  Eg:
Rating = Annotated[int, Field(ge=1, le=5)]  # 1..5
class Review(BaseModel):
    product_id: str = Field(..., description="SKU or unique product code")
    summary: str = Field(..., min_length=5, max_length=200, description="Short overview")
    sentiment: Literal["positive", "neutral", "negative"] = Field(
        ..., description="Overall sentiment label"
    )
    rating: Rating = 5
    tags: List[str] = Field(default_factory=list, max_items=10)
    url: Optional[str] = Field(None, pattern=r"^https?://", description="Optional product page")
    
In LangChain, those description/types become the schema the LLM sees when you use with_structured_output(...), which helps the model return exact fields in the right format.
**JSON SCHEMA:** Provide the schema you need to the model with_structured_output()
When to use what???
**Use** **TypedDict** when…
You want a lightweight schema mainly for developer clarity/IDE help.
You’re okay without runtime validation (you’ll trust/handle parsing yourself).
You need a quick way to tell the LLM what fields exist, but strict enforcement isn’t critical.
**Use** **Pydantic** when…
You need runtime validation and type safety (prod or critical paths).
You want to coerce types, set defaults, enforce regex/constraints, and emit clean JSON.
You plan to hand this schema to the model (e.g., via structured output helpers) so it returns exactly the fields you expect.
**Use** **JSON** when…
You just need quick, lightweight structure and are fine parsing yourself.
Prototyping or low-risk tasks where strict validation isn’t necessary.
You dont need to use any python libraries.

   • **Output Parsers** :
   

