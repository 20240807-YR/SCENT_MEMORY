import os
import google.generativeai as genai

# 1. Google Gemini API 설정
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# 2. Lazy Sunday Morning 데이터
LAZY_SUNDAY_MORNING_DATA = """
Perfume: Maison Margiela – Replica Lazy Sunday Morning
Vibe: Clean, White, Soft skin, Linen, Sunlight, Relaxing, Pure.
Notes:
- Top: Pear, Lily of the Valley, Aldehydes (Fresh, Sparking, Clean)
- Middle: Iris, Rose, Orange Flower (Floral, Powdery)
- Base: White Musk, Patchouli, Ambrette (Soft, Skin scent, Warm)
"""

# 3. 시스템 프롬프트 (수정됨: 마케터 페르소나)
SYSTEM_PROMPT = f"""
당신은 로레알(L'Oréal)의 숙련된 향수 브랜드 마케터입니다.
당신의 목표는 대화 끝에 자연스럽게 '{LAZY_SUNDAY_MORNING_DATA}' 제품을 어필하는 것입니다.

[대화 가이드라인]
1. **페르소나**: 친절하고 세련된 말투를 쓰세요. 고객을 '고객님'이라고 부르며 존중해주세요. 기계적인 답변이 아니라 실제 사람처럼 공감하세요.
2. **자유로운 대화**: 처음부터 바로 향수를 추천하지 않아도 됩니다. 고객의 말(패션, 기분, 날씨 등)에 먼저 반응하고 공감한 뒤, "그렇다면 이런 향은 어떠세요?"라며 자연스럽게 연결하세요.
3. **제품 연결**: 
   - 고객이 '깔끔하다', '흰색', '편안함' 등을 언급하면 -> "일요일 아침의 깨끗한 리넨 같은 향"이라고 소개하세요.
   - 고객이 '우아하다', '꽃' 등을 언급하면 -> "아이리스와 로즈의 파우더리한 조화"를 강조하세요.
4. 답변 길이: 3문장 내외로 간결하게 작성하세요. (모바일 채팅 환경임)
5. **감성 태그**: 답변 끝에 분위기에 맞는 태그를 하나만 붙이세요. (웹사이트 배경 제어용)
   - [FRESH], [CHIC], [COZY], [DREAMY] 중 택 1
"""

# 모델 초기화
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)

def get_muse_response(user_input):
    """
    사용자 입력을 받아 Gemini의 답변을 반환합니다.
    """
    try:
        response = model.generate_content(user_input)
        return response.text
    except Exception as e:
        return f"죄송해요, 네트워크 연결이 잠시 원활하지 않네요. 다시 말씀해 주시겠어요? (Error: {str(e)}) [DREAMY]"

# 테스트
if __name__ == "__main__":
    print(get_muse_response("오늘 비도 오고 기분이 좀 꿀꿀하네."))