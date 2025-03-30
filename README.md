# 🧠 EXAONE-DEEP RAG with FastAPI + FAISS + SentenceTransformer

한화생명 케어백H간병보험 무배당 상품요약서 PDF 문서를 FAISS 기반으로 임베딩 및 인덱싱하고, Ollama 기반 LLM(EXAONE)을 통해 질의응답을 수행하는 **RAG(Retrieval-Augmented Generation)** 시스템입니다.

> 🔍 **주요 특징**

- 📄 PDF 문서 파싱 및 슬라이딩 윈도우 청크
- 🧠 `jhgan/ko-sroberta-multitask` SentenceTransformer 기반 임베딩
- ⚡ FAISS로 빠른 벡터 검색
- 🧾 Ollama 로컬 API(EXAONE) 기반 질문응답
- 🧪 중복 문서 제거 및 프롬프트 최적화
- 🚀 FastAPI로 API 서비스

---

## 📂 프로젝트 구조
```plaintext
project/
├── app.py # FastAPI 앱 (LLM 질의 처리)
├── ingester.py # PDF 텍스트 추출 및 FAISS 인덱스 생성
├── retriever/
│
├── retriever.py # 검색기 (FAISS + 청크 로딩)
│
└── embedder.py # SentenceTransformer 임베딩
├── index/
│
├── faiss_index.bin # 저장된 벡터 인덱스
│
└── faiss_index.pkl # 저장된 청크 원문
└── data/
└── source.pdf # 질의 기반 문서 원본
```


| 구성요소    | 설명                                         |
| ----------- | -------------------------------------------- |
| 임베딩 모델 | `jhgan/ko-sroberta-multitask`                |
| 벡터 검색기 | Facebook FAISS (`faiss.IndexFlatL2`)         |
| LLM 응답    | Ollama EXAONE (`exaone-deep:7.8b`)           |
| 청크 방식   | 슬라이딩 윈도우 (기본 700자, 50자 overlap)   |
| 중복 제거   | `difflib.SequenceMatcher` 기반 유사도 필터링 |



![image](https://github.com/user-attachments/assets/d5ae865a-ec9c-48b8-ba81-6e0f1cab132b)
