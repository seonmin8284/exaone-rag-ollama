import faiss
import numpy as np
import pickle
from retriever.embedder import get_embedder

def build_faiss_index(docs, model, save_path):
    # ✅ 전체 문서를 슬라이스해서 chunk로 쪼개기
    all_chunks = []
    for doc in docs:
        chunks = split_document_into_chunks(doc)
        all_chunks.extend(chunks)

    # ✅ 쪼갠 chunk들을 벡터화
    embeddings = model.encode(all_chunks)

    # ✅ FAISS 인덱스 생성 및 저장
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))
    
    # ✅ 쪼갠 문서 저장
    with open(save_path.replace('.bin', '.pkl'), 'wb') as f:
        pickle.dump(all_chunks, f)

    faiss.write_index(index, save_path)


def search_docs(query, top_k=10):
    embedder = get_embedder()
    q_emb = embedder.encode([query])
    index = faiss.read_index("index/faiss_index.bin")
    with open("index/faiss_index.pkl", 'rb') as f:
        docs = pickle.load(f)
    D, I = index.search(np.array(q_emb), top_k)
    return [docs[i] for i in I[0]]

# pseudo-code 예시
def split_document_into_chunks(doc, chunk_size=700, overlap=50):
    # 슬라이딩 윈도우 방식으로 자름
    return [doc[i:i+chunk_size] for i in range(0, len(doc), chunk_size - overlap)]
