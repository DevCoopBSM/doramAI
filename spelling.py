# spelling.py
import re
import requests
from hanspell import spell_checker

def get_passport_key():
    """네이버에서 '네이버 맞춤법 검사기' 페이지에서 passportKey를 획득"""
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=네이버+맞춤법+검사기"
    res = requests.get(url)
    html_text = res.text
    match = re.search(r'passportKey=([^&"}]+)', html_text)
    return match.group(1) if match else None

def update_passport_key_in_spell_checker(passport_key):
    """spell_checker.py 파일의 passportKey를 업데이트"""
    spell_checker_file_path = './py-hanspell/hanspell/spell_checker.py'
    pattern = r"'passportKey': '.*'"
    with open(spell_checker_file_path, 'r', encoding='utf-8') as input_file:
        content = input_file.read()
    modified_content = re.sub(pattern, f"'passportKey': '{passport_key}'", content)
    with open(spell_checker_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(modified_content)

def check_spelling(text):
    """유효한 텍스트에 대해 hanspell로 맞춤법 검사 및 교정된 텍스트와 차이 여부 반환"""
    passport_key = get_passport_key()  # passportKey 갱신
    if passport_key:
        update_passport_key_in_spell_checker(passport_key)  # 새로운 passportKey로 업데이트
        result = spell_checker.check(text)

        # 교정된 텍스트
        corrected_text = result.checked
        
        # 차이 여부 확인
        difference = text != corrected_text
        
        return {
            "corrected_text": corrected_text,
            "difference": difference
        }
    else:
        print("passportKey를 찾을 수 없습니다.")
        return {
            "corrected_text": text,  # 교정에 실패했을 경우 원본 텍스트 반환
            "difference": False
        }
