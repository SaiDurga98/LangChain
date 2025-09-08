**#LANGCHAIN
#CODE IS IN MASTER BRANCH**
**What is LangChain?**

LangChain is an open-source framework for developing applications powered by large language models (LLMs).

**Why I'm Learning It**

Model-agnostic: The framework isn’t tied to one model or vendor. You can swap models (OpenAI, Anthropic, local Llama, Hugging Face, etc.) without rewriting your app logic—just change the model configuration.

Complete ecosystem: Provides concepts like chains, memory, and state handling to build robust LLM apps.

**What I Plan to Build**

Conversational chatbots

AI knowledge assistants

AI agents (tool-use / automation)

Workflow automation

Summarization / research helpers

**Core Ideas**
**LangChain Components (Models, Prompts, Chains, Memory, Indexes, Agents)**

These are the foundational building blocks in LangChain.

**Models**

In LangChain, models are the core interfaces to AI systems. They provide natural language understanding and context-aware text generation.

LLMs: “text in → text out”, ideal for single-turn prompts.

Chat Models: Built for conversations (system/user/assistant roles), handle history and tool calls.

Embeddings: Convert text to vectors for semantic search and retrieval.

**Prompts**

Prompts are the instructions you give the model to guide the output.

Write them as templates with variables for reusability and consistency.

For chat, use chat prompts with roles (system/human/ai), and inject past messages (via MessagesPlaceholder) when you need memory.

Prompt styles:

Dynamic & reusable prompts

Role-based prompts

Few-shot prompting

**Prompt Building Blocks**

**1) PromptTemplate (single text)**

Builds one string from a template and variables.

Best for single-turn tasks.

**2) ChatPromptTemplate (list of messages)**

Builds a sequence of messages (system/human/ai/…).

Best for chat, multi-turn, tool use, and role control.

**3) Messages & MessagesPlaceholder**

**Message types:**

**SystemMessage** – sets behavior/instructions

**HumanMessage** – user input

**AIMessage** – model’s prior reply (if replaying history)

**Tool/Function/ToolMessage** – tool-calling traces (agents)

**MessagesPlaceholder**: Injects a list of messages (e.g., conversation history) into a chat template at runtime.

Model.invoke(...)
├─ Single text (single-turn)
│  ├─ Static: "literal string"
│  └─ Dynamic: PromptTemplate → str
│
└─ List of messages (chat / multi-turn)
   ├─ Static: [SystemMessage, HumanMessage, ...]
   └─ Dynamic: ChatPromptTemplate (+ MessagesPlaceholder)

**Structured Outputs**

In LangChain, structured output means making the model return data in a well-defined format (e.g., JSON) instead of free-form text, so your app can parse and use it programmatically.

**Why We Need Structured Output**

Common scenarios:

Data extraction

API building

Agents/tool use (automation needs predictable fields)

**Ways to Get Structured Output**

A) **“Prompt it out”** (instruct the model to return JSON)
Write a clear instruction and a small schema in your prompt:
“Return the response in JSON with fields X, Y, Z.”

B) **with_structured_output(...)** -> accepts two kinds of inputs 1. json mode 2. function calling
LangChain provides a helper that binds a schema to your model so responses are coerced into that structure. Use it with a TypedDict or a Pydantic model.

**TypedDict**: Declares required keys & value types (type hints), but does not do runtime validation by itself.

**Pydantic**: Adds data parsing & validation, defaults, descriptions, optionals, coercion, regex/constraints, and can output .json()/.dict().

**JSON Schema**: When you use Pydantic with with_structured_output(...), the model sees a generated JSON Schema, which helps it return exact fields in the right format.

**TypedDict vs Pydantic vs JSON - when to use what**

Use TypedDict when…

You want a lightweight schema mainly for developer clarity/IDE help.

You’re okay without runtime validation (you’ll trust/handle parsing yourself).

You need a quick way to tell the LLM what fields exist, but strict enforcement isn’t critical.

Use Pydantic when…

You need runtime validation and type safety (prod or critical paths).

You want to coerce types, set defaults, enforce regex/constraints, and emit clean JSON.

You plan to hand this schema to the model (via structured output) so it returns exactly the fields you expect.

Use plain JSON when…

You just need quick, lightweight structure and are fine parsing yourself.

Prototyping or low-risk tasks where strict validation isn’t necessary.

You don’t need to use any Python libraries.

**Pydantic Field**—What It’s For

Field(...) lets you add defaults, validation rules, and metadata to model attributes. It powers both runtime validation and the generated JSON Schema.

Default values: Field(default=...) or default_factory=...

Validation constraints:

Numbers: gt, ge, lt, le, multiple_of

Strings/bytes: min_length, max_length, pattern (regex)

Arrays: min_items, max_items, unique_items

Schema & docs metadata: title, description, examples, deprecated, json_schema_extra

Aliasing & I/O control (v2): validation_alias, serialization_alias, alias (legacy), repr, exclude, frozen, validate_default

Example:

from typing import List, Optional, Literal, Annotated
from pydantic import BaseModel, Field

Rating = Annotated[int, Field(ge=1, le=5)]  # 1..5

class Review(BaseModel):
    product_id: str = Field(..., description="SKU or unique product code")
    summary: str = Field(..., min_length=5, max_length=200, description="Short overview")
    sentiment: Literal["positive", "neutral", "negative"] = Field(
        ..., description="Overall sentiment label"
    )
    rating: Rating = 5
    tags: List[str] = Field(default_factory=list, max_items=10)
    url: Optional[str] = Field(
        None, pattern=r"^https?://", description="Optional product page"
    )


In LangChain, these descriptions/types become the schema the LLM sees when you use with_structured_output(...), improving accuracy and formatting of returned data.

**Output Parsers**

Parsers help convert raw LLM responses into structured formats (JSON, CSV, Pydantic models, etc.)

**Types of Output Parsers:**

StringOutputParser

JSONOutputParser

StructuredOutputParser

PydanticOutputParser
