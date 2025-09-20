from ollama import embed, chat

embeddings = embed(model="qwen3:0.6b", input=["Here is an example sentence I will be embedding!", "Here's a second one!"])

print(len(embeddings['embeddings']))

response = chat(model='qwen3:0.6b', messages=[
  {
    'role': 'user',
    'content': 'Why did the chicken cross the road?',
  },
])

print(response.message.content)
