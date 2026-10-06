from retrieval.hybrid_search import hybrid_search

def retrieve(query: str, limit: int = 5):
   return hybrid_search(query, limit=limit)
