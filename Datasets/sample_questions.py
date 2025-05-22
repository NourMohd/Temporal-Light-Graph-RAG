import json
import random

# Load the JSON data from file
with open('MultiHopRAG.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Sample 100 items
sampled = random.sample(data, min(100, len(data)))

# Extract only 'query' and 'answer'
sampled_qas = [{'query': item['query'], 'answer': item['answer']} for item in sampled]

# Save the result to a new JSON file (optional)
with open('sampled_questions.json', 'w', encoding='utf-8') as f:
    json.dump(sampled_qas, f, indent=2, ensure_ascii=False)

