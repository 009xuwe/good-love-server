from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
# 开启跨域，Android APP请求不会被拦截
CORS(app)

# 鉴权密钥
REAL_AUTH_KEY = "Xiao_Pa_Cai_2026_XiaoPaCai_8a7f6d5c4b3a2918273645"

# 保活心跳接口，给cron‑job.org定时GET访问，防止Render休眠
@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"ok": True}), 200

@app.route("/api/checkAuth", methods=["POST"])
def check_auth():
    """接收APP上传的auth_key，做比对，返回valid布尔"""
    try:
        body = request.get_json()
        if not body or "auth_key" not in body:
            return jsonify({"valid": False}), 400
        client_key = str(body["auth_key"]).strip()
        is_ok = (client_key == REAL_AUTH_KEY.strip())
        return jsonify({"valid": is_ok})
    except Exception as e:
        return jsonify({"valid": False, "error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
