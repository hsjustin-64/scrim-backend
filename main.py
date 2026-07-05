# ✅ main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ⚠️ 1단계에서 복사해 둔 본인의 ID와 Secret으로 아래 값을 꼭 변경하세요!
CLIENT_ID = "1522531266421985341"
CLIENT_SECRET = "JRkjoz2-2w99M0t8kxSLLpUP-sc_mSri"
REDIRECT_URI = "https://scrim-hub-test.netlify.app"

@app.get("/")
def read_root():
    return {"message": "내전허브 백엔드 서버가 정상적으로 실행되었습니다!"}

# 📍 새로운 디스코드 로그인 처리 API
@app.get("/api/auth/discord")
def discord_login(code: str):
    # 1. 프론트엔드로부터 받은 '인증 코드(code)'를 디스코드 서버로 보내 진짜 '토큰'으로 교환합니다.
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    token_res = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
    token_json = token_res.json()

    if "access_token" not in token_json:
        return {"error": "토큰 발급 실패", "details": token_json}

    access_token = token_json["access_token"]

    # 2. 교환받은 진짜 '토큰'으로 유저의 프로필 정보를 요청합니다.
    user_res = requests.get("https://discord.com/api/users/@me", headers={"Authorization": f"Bearer {access_token}"})
    user_info = user_res.json()

    # 3. 유저 정보를 프론트엔드로 안전하게 전달합니다.
    return {"message": "로그인 성공", "user": user_info}


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 모든 주소(Netlify 포함)에서 접근 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)