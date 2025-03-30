from sentence_transformers import SentenceTransformer

def get_embedder():
    return SentenceTransformer("jhgan/ko-sroberta-multitask")
