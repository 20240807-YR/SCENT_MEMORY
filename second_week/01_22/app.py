import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

FIXED_REPLY = """It can feel clean and comforting at first.
But this sensation is not created by a specific ‘clean note’ or a familiar accord.

In this fragrance, the top is designed to fade quickly,
the heart avoids emotional emphasis,
and the base stays close to the skin instead of projecting.

This structure creates a quiet, disappearing presence rather than a noticeable scent.

Similar fragrances can reproduce the smell,
but they cannot explain why this sensation exists.

This is why Lazy Sunday Morning is not defined by how it smells,
but by why it was designed this way.

That is what makes it an Exception Fragrance.
"""

@app.route('/chat', methods=['POST'])
def chat():
    return jsonify({'reply': FIXED_REPLY})

if __name__ == '__main__':
    print("=== SCENT CANVAS 서버가 시작되었습니다 ===")
    print("=== 브라우저를 새로고침하고 채팅을 시도해보세요 ===")
    app.run(port=5000, debug=True)