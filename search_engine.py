from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_search(query, df, top_k=10):
    titles = df["title"].tolist()

    title_embeddings = model.encode(titles, convert_to_tensor=True)
    query_embedding  = model.encode(query,  convert_to_tensor=True)

    scores = util.cos_sim(query_embedding, title_embeddings)[0]
    scores = scores.cpu().numpy()

    results = df.copy()
    results["relevance"] = scores

    # Raised threshold — only return genuinely relevant results
    results = results[results["relevance"] > 0.30]

    # If nothing passes threshold return empty so dashboard shows "Not Found"
    if results.empty:
        return results

    # Normalize views to 0-1 scale
    max_views = results["views"].max() if results["views"].max() > 0 else 1
    results["views_score"] = results["views"] / max_views

    # Final score = 70% views + 30% match score
    results["final_score"] = (results["views_score"] * 0.7) + (results["relevance"] * 0.3)

    # Sort by final score highest to lowest
    results = results.sort_values("final_score", ascending=False).reset_index(drop=True)


from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_search(query, df, top_k=10):
    titles = df["title"].tolist()

    title_embeddings = model.encode(titles, convert_to_tensor=True)
    query_embedding  = model.encode(query,  convert_to_tensor=True)

    scores = util.cos_sim(query_embedding, title_embeddings)[0]
    scores = scores.cpu().numpy()

    results = df.copy()
    results["relevance"] = scores

    # Raised threshold — only return genuinely relevant results
    results = results[results["relevance"] > 0.30]

    # If nothing passes threshold return empty so dashboard shows "Not Found"
    if results.empty:
        return results

    # Normalize views to 0-1 scale
    max_views = results["views"].max() if results["views"].max() > 0 else 1
    results["views_score"] = results["views"] / max_views

    # Final score = 70% views + 30% match score
    results["final_score"] = (results["views_score"] * 0.7) + (results["relevance"] * 0.3)

    # Sort by final score highest to lowest
    results = results.sort_values("final_score", ascending=False).reset_index(drop=True)

    return results.head(top_k)