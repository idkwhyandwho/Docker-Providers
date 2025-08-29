from openai import OpenAI

# Only these 3 lines need to be changed from standard OpenAI code
client = OpenAI(
    base_url="http://localhost:8000/v1",  # Point to your local API
    api_key="your-local-api-key"          # Use your local API key
)

# Rest of the code remains exactly the same as with OpenAI
completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is Docker Model Runner?"}
    ]
)

print(completion.choices[0].message.content)

# Embeddings example
embedding = client.embeddings.create(
    model="text-embedding-ada-002",
    input="Hello, world!"
)

print(embedding.data[0].embedding)
