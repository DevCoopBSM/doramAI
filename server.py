# server.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
from typing import Dict, Any
from feedback import generate_feedback
from spelling import check_spelling  # spelling.py 임포트

# 로깅 설정
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
        logger.info(f"Received spelling check request: {request.text}")
        corrections = check_spelling(request.text)
        logger.info(f"Spelling check result: {corrections}")
        return {"corrections": corrections}
    except Exception as e:
        logger.error(f"Error in spelling check: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal Server Error",
                "message": str(e),
                "type": type(e).__name__
            }
        )

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
