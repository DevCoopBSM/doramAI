# server.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from feedback import generate_feedback
from spelling import check_spelling  # spelling.py 임포트

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

class FeedbackRequest(BaseModel):
    text: str
    categories: list[str]

class SpellingRequest(BaseModel):
    text: str

@app.post("/feedback/")
async def get_feedback(request: FeedbackRequest):
    try:
        feedback = generate_feedback(request.text, request.categories)
        return {"feedback": feedback}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/check-spelling/")
async def check_spelling_endpoint(request: SpellingRequest):
    try:
        corrections = check_spelling(request.text)
        return {"corrections": corrections}
    except Exception as e:
        # 에러 발생 시 요청 내용과 에러 메시지를 로그로 출력
        print(f"Error occurred while checking spelling for text: {request.text}")
        print(f"Error details: {str(e)}")
        
        # 클라이언트에게 더 구체적인 에러 메시지 반환
        raise HTTPException(status_code=500, detail={"error": "Internal Server Error", "message": str(e)})
