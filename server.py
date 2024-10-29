from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from feedback import generate_feedback

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

@app.post("/feedback/")
async def get_feedback(request: FeedbackRequest):
    try:
        feedback = generate_feedback(request.text, request.categories)
        return {"feedback": feedback}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
