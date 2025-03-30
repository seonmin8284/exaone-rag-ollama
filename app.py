from fastapi import FastAPI, Request
from retriever.retriever import search_docs  # ✅ 너가 구축한 벡터 검색기
import requests
from difflib import SequenceMatcher

app = FastAPI()


def clean_text(text: str) -> str:
    """불필요한 줄바꿈 제거 및 양쪽 공백 제거"""
    lines = text.splitlines()
    cleaned = [line.strip() for line in lines if line.strip()]
    return " ".join(cleaned)


def is_similar(a: str, b: str, threshold: float = 0.9) -> bool:
    """문서 중복 유사도 필터링"""
    return SequenceMatcher(None, a, b).ratio() > threshold


@app.post("/query")
async def query_llm(request: Request):
    try:
        req = await request.json()
        question = req.get("question", "").strip()

        if not question:
            return {"response": "질문을 입력해주세요."}

        # ✅ 1. 문서 검색
        raw_docs = search_docs(question)

        # ✅ 2. 중복 제거
        unique_docs = []
        for doc in raw_docs:
            if all(not is_similar(doc, u) for u in unique_docs):
                unique_docs.append(doc)

        # ✅ 3. context 구성 (문서당 300자 이내, 최대 3개)
        context_chunks = [clean_text(doc) for doc in unique_docs[:5]]  # 문서 수 늘림
        context = "\n\n".join(f"- {chunk[:1000]}" for chunk in context_chunks)  # 길이 확장


        # ✅ 4. 프롬프트 구성
        prompt = f"""[|system|][|endofturn|]
[|user|]다음 정보를 참고하여 질문에 답하세요:

{context}

질문: {question}
[|assistant|]"""

        print("🔥 최종 프롬프트:\n", prompt)

        # ✅ 5. Ollama API 요청
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "exaone-deep:7.8b",
                "prompt": prompt,
                "stream": False
            }
        )
        response.raise_for_status()

        # ✅ 6. 응답 반환
        result = response.json().get("response", "").strip()
        print("📥 Ollama 응답:", result)
        return {"response": result}

    except requests.exceptions.Timeout:
        print("⏱️ Ollama 응답 타임아웃!")
        return {"response": "응답이 너무 느립니다. 프롬프트 길이를 줄여주세요."}

    except Exception as e:
        print("❌ 오류 발생:", e)
        return {"response": f"에러 발생: {str(e)}"}
