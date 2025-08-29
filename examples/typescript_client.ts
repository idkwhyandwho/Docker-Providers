import OpenAI from 'openai';

// Only these 3 lines need to be changed from standard OpenAI code
const client = new OpenAI({
  baseURL: 'http://localhost:8000/v1',  // Point to your local API
  apiKey: 'your-local-api-key'          // Use your local API key
});

// Rest of the code remains exactly the same as with OpenAI
async function main() {
  const completion = await client.chat.completions.create({
    model: 'gpt-3.5-turbo',
    messages: [
      { role: 'system', content: 'You are a helpful assistant.' },
      { role: 'user', content: 'What is Docker Model Runner?' }
    ]
  });

  console.log(completion.choices[0].message.content);

  // Embeddings example
  const embedding = await client.embeddings.create({
    model: 'text-embedding-ada-002',
    input: 'Hello, world!'
  });

  console.log(embedding.data[0].embedding);
}

main().catch(console.error);
