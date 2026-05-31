import time
from typing import Tuple

class SemanticCache:
    def __init__(self):
        # A real implementation would use SQLite or FAISS for vectors
        # Using an O(1) dict for simulation
        self.db = {}

    def search(self, query: str) -> str | None:
        return self.db.get(query.lower().strip())

    def add(self, query: str, response: str):
        self.db[query.lower().strip()] = response


class EdgeModel:
    def __init__(self, model_path: str):
        self.model_path = model_path
        # Phase 1: self.llm = Llama(model_path=..., n_gpu_layers=-1)
        # n_gpu_layers=-1 offloads all layers to the Apple Silicon GPU

    def generate(self, prompt: str) -> str:
        time.sleep(1.5) # Simulated inference latency
        return f"Resolved by edge model [{self.model_path}]. Answer to: '{prompt}'"


class CloudAPI:
    def generate(self, prompt: str) -> str:
        time.sleep(3.0) # Simulated network latency and slow generation
        return f"Resolved by heavy model [Claude 3.5 Sonnet]. Answer to: '{prompt}'"


class CascadingRouter:
    def __init__(self):
        self.cache = SemanticCache()
        self.edge_model = EdgeModel(model_path="gemma-2b-q4_k_m.gguf")
        self.cloud_api = CloudAPI()

    def evaluate_complexity(self, prompt: str) -> str:
        """
        Complexity evaluation module.
        Will eventually use a fast classifier; for now uses keyword heuristics.
        """
        heavy_keywords = ["architecture", "optimize", "vulnerability", "analyze", "code"]
        if any(word in prompt.lower() for word in heavy_keywords):
            return "hard"
        return "simple"

    def process_request(self, prompt: str) -> Tuple[str, str, float]:
        """
        Main routing method.
        Returns: (Tier used, Response text, Elapsed time)
        """
        start_time = time.time()

        # --- TIER 1: Cache ($0) ---
        cached_response = self.cache.search(prompt)
        if cached_response:
            return "Tier 1 (Local Cache)", cached_response, time.time() - start_time

        # Complexity evaluation
        complexity = self.evaluate_complexity(prompt)

        # --- TIER 2: Local model ($0) ---
        if complexity == "simple":
            response = self.edge_model.generate(prompt)
            self.cache.add(prompt, response) # Cache for future requests
            return "Tier 2 (Local Edge AI)", response, time.time() - start_time

        # --- TIER 3: Cloud ($$$) ---
        response = self.cloud_api.generate(prompt)
        self.cache.add(prompt, response) # Cache the expensive response
        return "Tier 3 (Cloud API)", response, time.time() - start_time