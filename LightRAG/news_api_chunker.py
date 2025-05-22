import requests
import json
from datetime import datetime
import textwrap
import os
from newspaper import Article

NEWS_API_KEY = "5a2ed00ca6934e55a370ea2c2d912d00"  
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

def fetch_news(api_key, query=None, category=None, country="us", page_size=20):
    """
    Fetch news from NewsAPI.org
    """
    params = {
        "apiKey": api_key,
        "country": country,
        "pageSize": page_size
    }

    # params = {
    #     "apiKey": api_key,
    #     "country": country,
    #     "pageSize": page_size
    # }
    if query:
        params["q"] = query   
    if category:
        params['category'] = category
    try:
        response = requests.get(NEWS_API_URL, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return None

def chunk_text(text, chunk_size=1000):
    """
    Split text into chunks of approximately equal size
    """
    if not text:
        return []
    
    # Use textwrap to create chunks of appropriate size
    chunks = textwrap.wrap(text, width=chunk_size, break_long_words=False, 
                          replace_whitespace=False)
    return chunks

def process_news_into_chunks(news_data):
    """
    Process news data into chunks similar to the example provided
    """
    if not news_data or "articles" not in news_data:
        return []
    
    chunked_news = []
    
    for idx, article in enumerate(news_data["articles"]):
        # Extract basic article info
        title = article.get("title", "")
        source_name = article.get("source", {}).get("name", "")
        published_at = article.get("publishedAt", "")
        url = article.get("url", "")
        author = article.get("author", None)
        
        # Get content and description
        content = article.get("content", "")
        description = article.get("description", "")
        
        # Use content if available, otherwise use description
        #full_text = content if content else description
        if content and "[+" not in content:
            full_text = content
        else:
            print("Extracting Full Article from URL...")
            full_text = extract_full_article_text(url) or description

        
        # Create chunks from the content
        content_chunks = chunk_text(full_text)
        
        # Determine category (using a simple heuristic based on keywords)
        category = determine_category(title, description)
        
        # Create entry for each chunk
        for chunk_idx, chunk in enumerate(content_chunks):
            news_chunk = {
                "title": title,
                "author": author,
                "source": source_name,
                "published_at": published_at,
                "category": category,
                "url": url,
                "chunk": chunk,
                "chunk_idx": chunk_idx
            }
            chunked_news.append(news_chunk)
    
    return chunked_news

def determine_category(title, description):
    """
    Simple heuristic to determine category based on keywords.
    Ensures title/description are strings.
    """
    title = title or ""
    description = description or ""
    text = f"{title} {description}".lower()

    categories = {
        "technology": ["tech", "apple", "google", "microsoft", "app", "software", "hardware", "ai", "data"],
        "business":    ["business", "economy", "market", "stock", "invest", "finance", "company"],
        "entertainment": ["entertainment", "movie", "music", "celebrity", "film", "tv", "show"],
        "health":      ["health", "covid", "medical", "doctor", "virus", "disease", "vaccine"],
        "science":     ["science", "research", "study", "discover", "space"],
        "sports":      ["sport", "football", "soccer", "basketball", "game", "player", "team"],
    }

    for category, keywords in categories.items():
        if any(keyword in text for keyword in keywords):
            return category

    return "general"

def save_chunked_news(chunked_news, filename="api_news_chunks.json"):
    """
    Save chunked news to a JSON file
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(chunked_news, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(chunked_news)} news chunks to {filename}")

def display_chunked_news(chunked_news, num_to_display=100):
    """
    Display a sample of the chunked news for verification
    """
    if not chunked_news:
        print("No news chunks to display")
        return
    
    print(f"\nSample of {min(num_to_display, len(chunked_news))} news chunks:")
    for i in range(min(num_to_display, len(chunked_news))):
        print(json.dumps(chunked_news[i], indent=2))
        print("-" * 50)

def extract_full_article_text(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        print(f"Failed to extract article from {url}: {e}")
        return ""




def main():
    # Check if API key is set
    api_key = NEWS_API_KEY
    if api_key == "YOUR_API_KEY_HERE":
        api_key = input("Please enter your NewsAPI.org API key: ")
    
    # Fetch news
    print("Fetching news from NewsAPI.org...")
    news_data = fetch_news(api_key)
    
    if not news_data:
        print("Failed to fetch news. Please check your API key and internet connection.")
        return
    
    # Process news into chunks
    print(f"Processing {len(news_data.get('articles', []))} articles into chunks...")
    chunked_news = process_news_into_chunks(news_data)
    
    # Save chunked news
    save_chunked_news(chunked_news)
    
    # Display sample of chunked news
    display_chunked_news(chunked_news)



def fetch_news_dict(search_query=None):
    api_key = NEWS_API_KEY
    news_data = fetch_news(api_key, query=search_query)
    
    if not news_data:
        return
    
    chunked_news = process_news_into_chunks(news_data)
    return chunked_news


if __name__ == "__main__":
    main()
