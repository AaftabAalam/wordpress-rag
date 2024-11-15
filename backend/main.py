from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from embedding_generator import EmbeddingGenerator
from wordpress_integration import WordPressIntegration
from annoy_store import VectorStore
from summarization import Summarizer
from bs4 import BeautifulSoup
import numpy as np
import os
import logging
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


wp_integration = WordPressIntegration(base_url="https://s-q87765xbajj3l.eu1.wpsandbox.org")
embedding_generator = EmbeddingGenerator()
summarizer = Summarizer()

# Set up the vector store and index file path
index_file_path = os.path.join(os.path.dirname(__file__), "..", "annoy_indexes", "annoy_index.ann")
vector_store = VectorStore()

def load_or_create_index():
    try:
        vector_store.load_index(index_file_path)
    except Exception as e:
        logging.error(f"Error loading index: {e}")

        posts = wp_integration.fetch_posts()
        for post in posts:
            title = post['title']['rendered']
            content = post['content']['rendered']
            post_id = post['id']

            soup = BeautifulSoup(content, "html.parser")
            clean_content = soup.get_text()

            post_embedding = embedding_generator.generate_embedding(clean_content)
            vector_store.add_embedding(post_embedding, post_id)

        vector_store.build_index()
        vector_store.save_index(index_file_path)
        logging.info(f"Index built and saved to {index_file_path}")

# Call the function during startup
load_or_create_index()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI server"}

@app.post("/search/")
async def search(request: dict = Body(...)):
    try:
        query = request.get("text", "")

        if not query:
            raise HTTPException(status_code=400, detail="Query text is required")

        query_embedding = embedding_generator.generate_embedding(query)

        distances, doc_ids = vector_store.search(query_embedding, top_k=1)

        if not doc_ids:
            print("No results found, indexing posts...")

            posts = wp_integration.fetch_posts()

            for post in posts:
                title = post['title']['rendered']
                content = post['content']['rendered']
                post_id = post['id']

                soup = BeautifulSoup(content, "html.parser")
                clean_content = soup.get_text()

                post_embedding = embedding_generator.generate_embedding(clean_content)

                vector_store.add_embedding(post_embedding, post_id)

            vector_store.build_index()

            distances ,doc_ids = vector_store.search(query_embedding, top_k=1)

        posts_response = []
        for doc_id in doc_ids:
            post = wp_integration.fetch_post_by_id(doc_id)

            if not post:
                posts_response.append({
                    'title': 'No title',
                    'summary': 'No summary available'
                })
                continue

            title = post.get('title', {}).get('rendered', 'No title')
            content = post.get('content', {}).get('rendered', 'No content available')

            soup = BeautifulSoup(content, "html.parser")
            clean_content = soup.get_text()
            summary = summarizer.summarize_text(clean_content)

            posts_response.append({
                'title': title,
                'summary': summary
            })

        return JSONResponse(content={'response': posts_response})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during search: {str(e)}")

@app.post("/add_post_embeddings/")
async def add_post_embeddings(request: dict = Body(...)):
    try:
        post_id = request.get('post_id')
        post_text = request.get('post_text')

        if not post_id or not post_text:
            raise HTTPException(status_code=400, detail="Post ID and Post Text are required")

        post_embedding = embedding_generator.generate_embedding(post_text)

        vector_store.add_embedding(post_embedding, post_id)

        vector_store.build_index()

        return JSONResponse(content={'message': 'Post embedding added successfully'})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/save_index/")
async def save_index():
    try:
        vector_store.save_index(index_file_path)
        return JSONResponse(content={'message': 'Index saved successfully'})
    
    except Exception as e:
        logging.error(f"Failed to save index: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to save index: {str(e)}")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)