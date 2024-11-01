import os
from openai import OpenAI
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# API_KEY 가져오기
my_key = os.getenv("API_KEY")
client = OpenAI(api_key=my_key)


def generate_feedback(text, categories):
    keyword = ', '.join(categories)
    paragraphs = text.split('\n')
    
    feedback_responses = []

    for paragraph in paragraphs:
        if paragraph.strip():
            prompt = f"내가 쓴 소설의 가독성, 글의 구조 등을 포함해 피드백해 줘. 카테고리: {keyword}\n\n{paragraph}\n"
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=1
            )
            feedback = response.choices[0].message.content.strip()
            feedback_responses.append({"paragraph": paragraph, "feedback": feedback})

    return feedback_responses