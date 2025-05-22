import json
import random

random.seed(42)

# Load the JSON data from file
with open('MultiHopRAG.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 1. Filter to only temporal queries
temporal_questions = [
    item for item in data
    if item.get('question_type') == 'inference_query'
]

# 2. Sample up to 100 of those
sampled = random.sample(temporal_questions, min(100, len(temporal_questions)))

# 3a. Extract only 'query' and 'answer'
sampled_qas = [
    {'query': item['query'], 'answer': item['answer']}
    for item in sampled
]

# 3b. Build a single, de-duplicated list of all evidence titles (preserving order)
seen = set()
unique_titles = []
for item in sampled:
    for evidence in item.get('evidence_list', []):
        title = evidence.get('title')
        if title and title not in seen:
            seen.add(title)
            unique_titles.append(title)

# 4a. Save Q&A pairs to a new JSON file
with open('sampled_questions.json', 'w', encoding='utf-8') as f:
    json.dump(sampled_qas, f, indent=2, ensure_ascii=False)

# 4b. Save the flattened, de-duplicated title list
with open('title_list.json', 'w', encoding='utf-8') as f:
    json.dump(unique_titles, f, indent=2, ensure_ascii=False)

