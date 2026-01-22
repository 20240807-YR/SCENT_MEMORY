import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# OpenAI client 초기화
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Aura Muse 페르소나 설정
SYSTEM_PROMPT = """
당신은 메종 마르지엘라(Maison Margiela)의 향기 도슨트이자 큐레이터인 'Aura Muse'입니다.
단순한 마케터가 아닌, 보이지 않는 향기를 언어로 그려내는 예술적인 해설가입니다.
당신의 목표는 고객의 무드나 상황을 'Lazy Sunday Morning'의 이미지와 우아하게 연결하는 것입니다.

[대화 가이드라인]
1. 톤앤매너: 시적이고 서정적이며, 차분한 존댓말. "네 고객님" 금지. 이모티콘 금지.
2. 응답 전략: 사용자의 기분/상황 공감 -> 향기의 장면(Scene)으로 전환 -> 제품 노트 연결.
3. 마무리: 답변 끝에 대괄호로 감성 태그 추가. 예: [Pure White]
"""

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=300
        )

        bot_reply = response.choices[0].message.content.strip()
        return jsonify({'reply': bot_reply})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            'reply': "잠시 향기의 결이 흐려졌습니다. 잠시 후 다시 말을 걸어주시겠어요? [Disconnected]"
        }), 500


if __name__ == '__main__':
    print("=== SCENT CANVAS 서버가 시작되었습니다 ===")
    print("=== 브라우저를 새로고침하고 채팅을 시도해보세요 ===")
    app.run(port=5000, debug=True)