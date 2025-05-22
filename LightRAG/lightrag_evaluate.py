import os
import json
import time
import asyncio
import nest_asyncio
import numpy as np
from tqdm.auto import tqdm
from dotenv import load_dotenv
from google import genai
from google.genai import types
from sentence_transformers import SentenceTransformer
from lightrag.utils import EmbeddingFunc
from lightrag import LightRAG, QueryParam
from lightrag.kg.shared_storage import initialize_pipeline_status
import argparse

# Apply nest_asyncio to solve event loop issues
nest_asyncio.apply()

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

WORKING_DIR = "/content/LightRAGTest/LightRAG/news_index"


async def llm_model_func(
    prompt, system_prompt=None, history_messages=None, keyword_extraction=False, **kwargs
):
    client = genai.Client(api_key=gemini_api_key)
    history_messages = history_messages or []

    # Build combined prompt
    combined = ""
    if system_prompt:
        combined += f"{system_prompt}\n"
    for msg in history_messages:
        combined += f"{msg['role']}: {msg['content']}\n"
    combined += f"user: {prompt}"

    # Call Gemini
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=[combined],
        config=types.GenerateContentConfig(max_output_tokens=500, temperature=0.1),
    )
    return response.text


async def embedding_func(texts: list[str]) -> np.ndarray:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return model.encode(texts, convert_to_numpy=True)


async def initialize_rag():
    rag = LightRAG(
        working_dir=WORKING_DIR,
        llm_model_func=llm_model_func,
        embedding_func=EmbeddingFunc(
            embedding_dim=384,
            max_token_size=8192,
            func=embedding_func,
        ),
    )
    await rag.initialize_storages()
    await initialize_pipeline_status()
    return rag


def main():
    parser = argparse.ArgumentParser(
        description="Run RAG predictions on a set of sampled questions"
    )
    parser.add_argument(
        "-i", "--input", required=True,
        help="Path to the input JSON (list of {query, answer})"
    )
    parser.add_argument(
        "-o", "--output", required=True,
        help="Path to write output JSON with predictions"
    )
    args = parser.parse_args()

    # 1. Read in the sampled questions
    with open(args.input, 'r', encoding='utf-8') as f:
        samples = json.load(f)

    # 2. Initialize your RAG system once
    rag = asyncio.run(initialize_rag())

    results = []

    # 3. Loop with progress bar
    for item in tqdm(samples, desc="Querying RAG"):
        query = item['query']
        prediction = rag.query(
            query=query,
            param=QueryParam(
                mode="hybrid",
                top_k=5,
                response_type="single line"
            )
        )

        results.append({
            'query': query,
            'answer': item['answer'],
            'prediction': prediction
        })

        # 4. Write incremental results to disk
        with open(args.output, 'w', encoding='utf-8') as out_f:
            json.dump(results, out_f, indent=2, ensure_ascii=False)

        # 5. Throttle
        time.sleep(0.5)

    print(f"Wrote {len(results)} predictions to {args.output}")


if __name__ == "__main__":
    main()
