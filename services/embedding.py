from sentence_transformers import SentenceTransformer

# Cache models to avoid reloading
_MODEL_CACHE = {}

MODEL_MAP = {
    "minilm": "sentence-transformers/all-MiniLM-L6-v2",
    "distilbert": "distilbert-base-nli-stsb-mean-tokens",
    "sbert": "sentence-transformers/all-mpnet-base-v2"
}


def get_sentence_embeddings(sentences: list, model_name: str):
    if model_name not in MODEL_MAP:
        raise ValueError(f"Unsupported model: {model_name}")

    if model_name not in _MODEL_CACHE:
        _MODEL_CACHE[model_name] = SentenceTransformer(
            MODEL_MAP[model_name]
        )

    model = _MODEL_CACHE[model_name]

    embeddings = model.encode(
        sentences,
        normalize_embeddings=True
    )

    return embeddings
