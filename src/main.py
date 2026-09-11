import os
import torch
from typing import Optional
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pymilvus import MilvusClient
from sentence_transformers import SentenceTransformer

app = FastAPI(title="TownPulse Semantic Search")

# 1. Mount Static Files directory
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

embed_model: Optional[SentenceTransformer] = None

COLLECTION_NAME = "townpulse_places"
DB_PATH = os.path.abspath("data/townpulse.db")


@app.on_event("startup")
def startup_event():
    global embed_model
    
    # Select compute device (MPS for Apple Silicon, CUDA, or CPU fallback)
    device = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Loading embedding model onto device: {device.upper()}")
    embed_model = SentenceTransformer("all-MiniLM-L6-v2", device=device)

class SearchRequest(BaseModel):
    query: str
    age_group: Optional[str] = None
    limit: int = 5


@app.post("/api/search")
def search_places(req: SearchRequest):
    # Ensure collection is loaded before querying
    milvus_client = MilvusClient(DB_PATH)
    milvus_client.load_collection(collection_name=COLLECTION_NAME)

    query_vector = embed_model.encode(req.query).tolist()
    
    results = milvus_client.search(
        collection_name=COLLECTION_NAME,
        data=[query_vector],
        limit=req.limit,
        output_fields=["place_name", "place_category", "location_area", "description"]
    )
    matches = []
  # Milvus returns a list of lists (one per query vector in data=[...])
    if results and len(results) > 0:
        for hit in results[0]:
            # Handle both dictionary output or Hit objects safely
            entity = hit.get("entity", {}) if isinstance(hit, dict) else hit.entity
            distance = (
                hit.get("distance", 0.0)
                if isinstance(hit, dict)
                else getattr(hit, "distance", 0.0)
            )

            matches.append({
                "score": round(distance, 4),
                "name": entity.get("place_name"),
                "category": entity.get("place_category"),
                "location": entity.get("location_area"),
                "description": entity.get("description"),
            })

    return {"query": req.query, "results": matches}


# Serve the main index.html file
@app.get("/")
def read_root():
    return FileResponse(os.path.join(static_dir, "index.html"))