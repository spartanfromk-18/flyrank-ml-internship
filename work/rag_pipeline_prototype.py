import time
import hashlib
from typing import Dict, List, Tuple

class ContextualSemanticCache:
    """In-memory prefix and query cache to bypass redundant vector retrieval and LLM calls."""
    def __init__(self, ttl_seconds: int = 3600):
        self.store: Dict[str, Tuple[str, float]] = {}
        self.ttl = ttl_seconds
        self.hits = 0
        self.misses = 0

    def _hash_query(self, query: str, context_id: str) -> str:
        normalized = f"{context_id}::{query.strip().lower()}"
        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

    def get(self, query: str, context_id: str) -> str | None:
        key = self._hash_query(query, context_id)
        if key in self.store:
            response, timestamp = self.store[key]
            if time.time() - timestamp < self.ttl:
                self.hits += 1
                return response
        self.misses += 1
        return None

    def set(self, query: str, context_id: str, response: str) -> None:
        key = self._hash_query(query, context_id)
        self.store[key] = (response, time.time())


class MultiAgentRAGPipeline:
    """Two-stage Router + Retriever Agent pipeline with contextual caching."""
    def __init__(self):
        self.cache = ContextualSemanticCache()
        self.knowledge_base = {
            "lightgbm_ndcg": "The LightGBM Ranker achieved 0.814 NDCG@20 on the sealed June 2026 holdout.",
            "baseline_rule": "The 12-month calendar age rule baseline achieved 0.642 NDCG@20 (+0.172 lift).",
            "data_contract": "Trained on 12,450 production search URLs with zero client-identifying PII."
        }

    def router_agent(self, query: str) -> str:
        q = query.lower()
        if "ndcg" in q or "score" in q:
            return "lightgbm_ndcg"
        elif "baseline" in q or "rule" in q:
            return "baseline_rule"
        return "data_contract"

    def query(self, user_query: str, session_context: str = "default") -> Tuple[str, float, bool]:
        t0 = time.perf_counter()

        # 1. Check Contextual Cache first
        cached = self.cache.get(user_query, session_context)
        if cached is not None:
            latency_ms = (time.perf_counter() - t0) * 1000
            return cached, latency_ms, True

        # 2. Cold Path: Router Agent -> Vector/KB Lookup -> Synthesis (Simulated 420ms cold LLM/Retrieval latency)
        time.sleep(0.42)
        route_key = self.router_agent(user_query)
        retrieved_chunk = self.knowledge_base[route_key]
        synthesized_answer = f"[Synthesized via {route_key}] {retrieved_chunk}"

        # 3. Populate Cache
        self.cache.set(user_query, session_context, synthesized_answer)
        latency_ms = (time.perf_counter() - t0) * 1000
        return synthesized_answer, latency_ms, False


if __name__ == "__main__":
    pipeline = MultiAgentRAGPipeline()
    test_queries = [
        "What was the LightGBM NDCG score?",
        "How did the baseline rule perform?",
        "What was the LightGBM NDCG score?",  # Repeat query (Cache Hit)
        "What is the data contract?",
        "How did the baseline rule perform?",  # Repeat query (Cache Hit)
    ]

    cold_latencies: List[float] = []
    warm_latencies: List[float] = []

    print("=== Running Multi-Agent RAG Contextual Cache Benchmark ===")
    for idx, q in enumerate(test_queries, 1):
        ans, ms, is_cached = pipeline.query(q, session_context="eval_session_01")
        status = "CACHE HIT" if is_cached else "COLD MISS"
        print(f"Query {idx} [{status}] ({ms:.2f} ms): {ans}")
        if is_cached:
            warm_latencies.append(ms)
        else:
            cold_latencies.append(ms)

    avg_cold = sum(cold_latencies) / len(cold_latencies)
    avg_warm = sum(warm_latencies) / len(warm_latencies)
    hit_rate = (pipeline.cache.hits / len(test_queries)) * 100
    print(f"\nBenchmark Summary -> Cold Avg: {avg_cold:.1f}ms | Warm Cached Avg: {avg_warm:.2f}ms | Hit Rate: {hit_rate:.1f}%")
