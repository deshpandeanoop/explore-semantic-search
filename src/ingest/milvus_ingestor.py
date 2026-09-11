import csv
from pymilvus import MilvusClient
from sentence_transformers import SentenceTransformer


def ingest_townpulse_data(
    csv_path: str = "data/town_pulse_dataset.csv",
    db_path: str = "data/townpulse.db",
    collection_name: str = "townpulse_places",
    model_name: str = "all-MiniLM-L6-v2"
) -> MilvusClient:
    """Reads TownPulse CSV data, generates dense embeddings, and indexes

    entities into a local Milvus Lite collection.

    Returns the initialized MilvusClient instance.
    """
    # 1. Initialize local Milvus Lite DB & Embedding Model
    client = MilvusClient(db_path)
    model = SentenceTransformer(model_name)

    # 2. Recreate collection for fresh ingestion
    if client.has_collection(collection_name):
        client.drop_collection(collection_name)

    client.create_collection(
        collection_name=collection_name,
        dimension=384,  # 384 dimensions for all-MiniLM-L6-v2
        metric_type="COSINE",
        auto_id=False
    )

    # 3. Process CSV into vector points + metadata payload
    data_to_insert = []

    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Construct semantic text for embedding
            semantic_text = (
                f"Place: {row['place_name']}\n"
                f"Category: {row['place_category']}\n"
                f"Location: {row['location_area']}\n"
                f"Description: {row['description']}"
            )

            vector = model.encode(semantic_text).tolist()

            entity = {
                "id": int(row["id"]),
                "vector": vector,
                "place_name": row["place_name"],
                "place_category": row["place_category"],
                "target_gender": row["target_gender"],
                "age_group": row["age_group"],
                "location_area": row["location_area"],
                "description": row["description"]
            }
            data_to_insert.append(entity)

    # 4. Insert records in bulk
    client.insert(collection_name=collection_name, data=data_to_insert)
    print(f"Successfully ingested {len(data_to_insert)} items into '{collection_name}'.")

    return client


if __name__ == "__main__":
    # Example execution when run directly
    client = ingest_townpulse_data()