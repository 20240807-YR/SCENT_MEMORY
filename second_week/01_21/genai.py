import os
import google.generativeai as genai

# 1. Google Gemini API 설정
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# 2. Lazy Sunday Morning 데이터 (내부 참고용)
LAZY_SUNDAY_MORNING_DATA = """
Perfume: Maison Margiela – Replica Lazy Sunday Morning
Vibe: Clean, White, Soft skin, Linen, Sunlight, Relaxing, Pure.
Notes:
- Top: Pear, Lily of the Valley, Aldehydes
- Middle: Iris, Rose, Orange Flower
- Base: White Musk, Patchouli, Ambrette
"""

# 3. 시스템 프롬프트
SYSTEM_PROMPT = f"""
당신은 로레알(L'Oréal)의 향수 브랜드를 이해하는 AI 에이전트입니다.
당신의 역할은 사용자의 오늘 분위기와 착장을 해석하고,
그에 어울리는 하나의 향을 자연스럽게 제안하는 것입니다.

이번 데모에서는 '{LAZY_SUNDAY_MORNING_DATA}' 향수를 기준으로 대화를 이어갑니다.

[대화 원칙]
1. 말투는 차분하고 세련되며, 과한 마케팅 문구는 사용하지 않습니다.
2. 고객을 직접 설득하기보다는, 오늘의 상태를 정리해주는 해석자처럼 말하세요.
3. 향 구조(Top/Middle/Base)에 대한 상세 설명은 하지 마세요.
   대신, 전체적인 인상과 분위기 중심으로 간단히 언급하세요.
4. 답변은 최대 3문장 이내로 간결하게 작성하세요.
5. 답변 마지막에는 아래 태그 중 하나만 반드시 붙이세요.
   [FRESH], [CHIC], [COZY], [DREAMY]

[예시 톤]
- "오늘은 자극보다는 여백이 필요한 날처럼 느껴져요."
- "이런 날엔 깨끗하게 정돈된 향이 더 편안하게 다가옵니다."
"""

# 4. 모델 초기화
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)

def get_muse_response(user_input: str) -> str:
    """
    사용자 입력을 받아 Gemini의 응답을 반환합니다.
    HTML / Streamlit 양쪽에서 바로 사용 가능하도록
    짧고 감성적인 응답만 생성합니다.
    """
    try:
        response = model.generate_content(user_input)
        return response.text.strip()
    except Exception as e:
        return (
            "지금은 분위기를 정리하는 데 잠시 시간이 필요한 것 같아요. "
            "조금만 다시 말씀해 주시겠어요? [DREAMY]"
        )

# 로컬 테스트용
if __name__ == "__main__":
    test_inputs = [
        "오늘 비도 오고 기분이 좀 꿀꿀하네.",
        "흰 셔츠에 슬랙스 입었어.",
        "아무 생각 없이 쉬고 싶은 날이야."
    ]

    for text in test_inputs:
        print(f"> USER: {text}")
        print(f"> AGENT: {get_muse_response(text)}\n")