from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
# LLM (import openAI)= plain text-in → text-out (completion style).
# ChatModel (import ChatOpenAI) = list of messages-in → message-out (chat/completions with roles, tool-calls, etc.).
# ChatModel Pick ChatModel by default for modern apps: system prompts, conversation history, function/tool calling, better structured outputs.
# Pick LLM if you’re integrating with legacy “text completion” endpoints or doing single-shot generations where roles/history don’t matter.
# Temperature is a parameter that controls the randomness of output. It affects how creative or deterministic the responses are.
# Lower values (0.0-0.3) - More deterministic and predictable
# Higher values (0.7-1.5) - More random, creative and diverse
# max_completion_tokens can restrict the number of tokens to be generated in the output
chatModel = ChatOpenAI(model='gpt-4', temperature= 0.3, max_completion_tokens=100)
result = chatModel.invoke("who is Narendra Modi")
print(result.content)