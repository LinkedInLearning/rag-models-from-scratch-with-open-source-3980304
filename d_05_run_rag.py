import sys
from d_02_prepare_content import search_by_query
from ollama import chat

query = "Is the Dominican Republic a member of the United Nations?"
if len(sys.argv) > 1:
    query = sys.argv[1]

context = search_by_query(query)

prompt = f"<|content_start>{context} \
<|content_end> {query}"

# print(f"Prompt: {prompt}")

response = chat(model='qwen3:0.6b', messages=[
  {
    'role': 'user',
    'content': prompt,
  },
])

print(response.message.content)
