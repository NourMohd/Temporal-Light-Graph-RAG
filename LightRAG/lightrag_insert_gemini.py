import os
import numpy as np
from google import genai
from google.genai import types
from dotenv import load_dotenv
from lightrag.utils import EmbeddingFunc
from lightrag import LightRAG, QueryParam
from sentence_transformers import SentenceTransformer
from lightrag.kg.shared_storage import initialize_pipeline_status
from news_api_chunker import fetch_news_dict
from dateutil import parser
import asyncio
import nest_asyncio

# Apply nest_asyncio to solve event loop issues
nest_asyncio.apply()

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

WORKING_DIR = "/content/LightRAGTest/LightRAG/news_index"

async def llm_model_func(
    prompt, system_prompt=None, history_messages=[], keyword_extraction=False, **kwargs
):
    # 1. Initialize the GenAI Client with your Gemini API Key
    client = genai.Client(api_key=gemini_api_key)

    # 2. Combine prompts: system prompt, history, and user prompt
    if history_messages is None:
        history_messages = []

    combined_prompt = ""
    if system_prompt:
        combined_prompt += f"{system_prompt}\n"

    for msg in history_messages:
        # Each msg is expected to be a dict: {"role": "...", "content": "..."}
        combined_prompt += f"{msg['role']}: {msg['content']}\n"

    # Finally, add the new user prompt
    combined_prompt += f"user: {prompt}"

    # 3. Call the Gemini model
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=[combined_prompt],
        config=types.GenerateContentConfig(max_output_tokens=500, temperature=0.1),
    )

    # 4. Return the response text
    return response.text


async def embedding_func(texts: list[str]) -> np.ndarray:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings


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



def chunk_to_string(chunk: dict, date_format: str = "%B %d, %Y %H:%M UTC") -> str:
    """
    Convert a news‐chunk dict into one formatted string.

    Parameters:
    - chunk: dict with keys like title, author, source, published_at (ISO8601),
      url, category, chunk, chunk_idx.
    - date_format: strftime format to render the timestamp.

    Returns:
    - A single string, e.g.:
      "Title: …\nDate: …\nSource: …\nAuthor: …\nCategory: …\nURL: …\nChunk #0: …"
    """
    # parse and prettify the date, if possible
    try:
        dt = parser.isoparse(chunk.get("published_at"))
        published = dt.strftime(date_format)
    except Exception:
        published = chunk.get("published_at", "Unknown date")

    parts = [
        f"Title: {chunk.get('title', '').strip()}",
        f"Date: {published}",
        f"Source: {chunk.get('source', '').strip()}",
    ]

    # only include author/category if present
    if chunk.get("author"):
        parts.append(f"Author: {chunk['author'].strip()}")
    if chunk.get("category"):
        parts.append(f"Category: {chunk['category'].strip()}")

    # url
    if chunk.get("url"):
        parts.append(f"URL: {chunk['url'].strip()}")

    # finally the chunk content
    text = chunk.get("chunk", "").strip().replace("\n", " ")
    parts.append(f"Chunk Text: {text}")

    # join with double-newlines (or single newlines if you prefer)
    return "\n\n".join(parts)

def main():
    # Initialize RAG instance
    rag = asyncio.run(initialize_rag())

    search_query = input("Retrieve News About: ")
    retrieved_chunks = fetch_news_dict(search_query=search_query)

    if retrieved_chunks:
        for chunk in retrieved_chunks:
            chunk_str = chunk_to_string(chunk)
            print(chunk_str)
            rag.insert(chunk_str)
    else:
        print("No News Articles Found")


    

if __name__ == "__main__":
    main()
