from retriever.embedder import get_embedder
from retriever.retriever import build_faiss_index
from PyPDF2 import PdfReader

reader = PdfReader("data/source.pdf")
text = "\n".join([page.extract_text() for page in reader.pages])

# Split text into chunks
chunks = text.split("\n\n")  # 간단한 청크 방식

# 임베딩 후 FAISS 인덱스 생성
embedder = get_embedder()
build_faiss_index(chunks, embedder, save_path="index/faiss_index.bin")
