# Open source models that can be modified, downloaded and modified/fine-tuned and deployed anywhere like LLaMA, Mixtral, Falcon
# OpenAI, Anthropic Claude, Google Gemini are all closed source LLMs and use vendor APIs to interact with them
# HuggingFace - Repository of open-source LLMs - can use Hugging Face inference API

# _chatmodel_huggingFace.py
# _chatmodel_huggingFace.py
import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from huggingface_hub import InferenceClient

load_dotenv()

# IMPORTANT: use this exact var name (or HF_TOKEN)
hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
if not hf_token:
    raise RuntimeError("HUGGINGFACEHUB_API_TOKEN is not set. Put it in your .env")

client = InferenceClient(
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    token=hf_token,
    provider="hf-inference",           # <-- critical: avoid featherless router
)

# Use the plain text-generation endpoint (avoids the featherless provider issue)
llm = HuggingFaceEndpoint(
    repo_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    task="text-generation",
    client=client, 
    huggingfacehub_api_token=hf_token,
    max_new_tokens=256,
    temperature=0.2,
)
chat = ChatHuggingFace(llm=llm)

res = chat.invoke("who is Narendra Modi")
print(res.content)    



