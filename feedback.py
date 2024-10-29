from openai import OpenAI
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 로드
load_dotenv()

# API_KEY가져옴
my_key = os.getenv("API_KEY")
client = OpenAI(api_key=my_key)

def generate_feedback(text, categories):
    keyword = ', '.join(categories)
    paragraphs = text.split('\n')
    
    feedback_responses = []

    for paragraph in paragraphs:
        if paragraph.strip():  # 문단이 비어있지 않은 경우에만 처리
            prompt = f"내가 쓴 소설의 문단을 피드백 해줘. 카테고리: {keyword}\n\n{paragraph}\n"
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=1
            )
            feedback = response.choices[0].message.content.strip()
            feedback_responses.append({"paragraph": paragraph, "feedback": feedback})

    return feedback_responses
