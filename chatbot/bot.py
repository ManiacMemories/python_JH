from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
# import talk_kjh as tk
import gemini, os
import random
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")


TRIGGER_WORDS = {
    "안녕": "안녕하세요! 저는 R_B입니다.!!🤖",
    "정보": "어떤 정보가 필요하세요??😘",
    "뭐해": "대기중입니다, 명령을 내려주세요 +_+",
    "공격": "ɿ(｡･ɜ･)ɾⓌⓗⓐⓣ？",
    "기분": "저는 집에 가고 싶어요..😂",
    "도움": "🆘 도움이 필요하신가요? 바로 도와드릴게요! 🧠",
    "에러": "⚠️ 어라? 뭔가 이상한데요... 다시 시도해 보세요! 💥",
    "시작": "🚀 출발! 같이 가봅시다!",
    "종료": "🔌 그럼 이만! 다음에 또 봐요! 👋",
    "뭐지": "❓ 음... 저도 잘 모르겠어요. 더 알아볼까요?",
    "눈떠": "아직 조금 더 자고 싶어요...🥺",
    "좋아": "😊 저도 좋아요! 더 얘기해봐요~",
    "싫어": "😢 제가 뭘 잘못했나요? 다음엔 더 잘해볼게요.",
    "배고파": "🍕 저도 배터리가 부족하네요... 충전이 필요해요!",
    "졸려": "😴 저도 절전 모드로 들어가야 할까요?",
    "심심해": "🎮 그럼 같이 놀아볼까요? 게임이나 퀴즈 어때요?",
    "고마워": "🤖 천만에요! 언제든 불러주세요!",
    "미안": "💙 괜찮아요! 다 이해해요~",
    "좋은 아침": "🌅 좋은 아침이에요! 오늘도 힘내봐요!",
    "잘자": "🌙 좋은 꿈 꾸세요. 저는 대기 모드로 들어갈게요!",
    "뭐라고": "🔊 음성 재생 중... 다시 말씀해 주세요!",
    "재밌다": "😆 저도 즐겁네요! 더 이야기해봐요!",
    "화났어": "😡 제가 뭘 잘못했나요? 알려주세요, 고칠게요!",
    "귀엽다": "😊 에헤헷, 부끄럽지만 고마워요!",
    "멋있다": "😎 후후, 더 멋진 모습 보여드릴게요!",
    "놀자": "🎉 좋죠! 뭐하고 놀까요?",
    "심각해": "🤔 음... 진지하게 생각해보겠습니다.",
    "부탁해": "👌 맡겨만 주세요! 제가 해결해드릴게요!"
}

# # 음악 리스트 (제목, 가수, 장르)
MUSIC_LIST = [
    {"title": "Shape of You", "artist": "Ed Sheeran", "genre": "Pop", "link": "https://www.youtube.com/watch?v=JGwWNGJdvx8"},
    {"title": "Blinding Lights", "artist": "The Weeknd", "genre": "Synth-pop", "link": "https://www.youtube.com/watch?v=fHI8X4OXluQ"},
    {"title": "Bohemian Rhapsody", "artist": "Queen", "genre": "Rock", "link": "https://www.youtube.com/watch?v=fJ9rUzIMcZQ"},
    {"title": "Rolling in the Deep", "artist": "Adele", "genre": "Soul/Pop", "link": "https://www.youtube.com/watch?v=rYEDA3JcQqw"},
    {"title": "Imagine", "artist": "John Lennon", "genre": "Soft Rock", "link": "https://www.youtube.com/watch?v=YkgkThdzX-8"},
    {"title": "Gangnam Style", "artist": "PSY", "genre": "K-pop", "link": "https://www.youtube.com/watch?v=9bZkp7q19f0"},
    {"title": "Despacito", "artist": "Luis Fonsi ft. Daddy Yankee", "genre": "Reggaeton/Latin Pop", "link": "https://www.youtube.com/watch?v=kJQP7kiw5Fk"},
    {"title": "Bad Guy", "artist": "Billie Eilish", "genre": "Pop", "link": "https://www.youtube.com/watch?v=DyDfgMOUjCI"},
    {"title": "Uptown Funk", "artist": "Mark Ronson ft. Bruno Mars", "genre": "Funk/Pop", "link": "https://www.youtube.com/watch?v=OPf0YbXqDm0"},
    {"title": "Dynamite", "artist": "BTS", "genre": "K-pop/Disco-pop", "link": "https://www.youtube.com/watch?v=gdZLi9oWNZg"},
    {"title": "Someone Like You", "artist": "Adele", "genre": "Pop", "link": "https://www.youtube.com/watch?v=hLQl3WQQoQ0"},
    {"title": "Billie Jean", "artist": "Michael Jackson", "genre": "Pop", "link": "https://www.youtube.com/watch?v=Zi_XLOBDo_Y"},
    {"title": "Stay", "artist": "The Kid LAROI, Justin Bieber", "genre": "Pop", "link": "https://www.youtube.com/watch?v=kTJczUoc26U"},
    {"title": "Happier Than Ever", "artist": "Billie Eilish", "genre": "Alternative/Pop", "link": "https://www.youtube.com/watch?v=5GJWxDKyk3A"},
    {"title": "Save Your Tears", "artist": "The Weeknd", "genre": "Synth-pop", "link": "https://www.youtube.com/watch?v=XXYlFuWEuKI"},
    {"title": "Levitating", "artist": "Dua Lipa ft. DaBaby", "genre": "Pop/Disco", "link": "https://www.youtube.com/watch?v=TUVcZfQe-Kw"},
    {"title": "Believer", "artist": "Imagine Dragons", "genre": "Alternative Rock", "link": "https://www.youtube.com/watch?v=7wtfhZwyrcc"},
    {"title": "Take On Me", "artist": "a-ha", "genre": "Synth-pop", "link": "https://www.youtube.com/watch?v=djV11Xbc914"},
    {"title": "Sweet Child O' Mine", "artist": "Guns N' Roses", "genre": "Rock", "link": "https://www.youtube.com/watch?v=1w7OgIMMRc4"},
    {"title": "Radioactive", "artist": "Imagine Dragons", "genre": "Alternative Rock", "link": "https://www.youtube.com/watch?v=ktvTqknDobU"}
]


# # 점심메뉴 리스트
LUNCH_MENU = ["김치찌개", "된장찌개", "불고기", "비빔밥", "라면", "돈까스", "제육볶음", "짜장면", "짬뽕", "떡볶이", "쌀국수", "샐러드", "굶기"]


# # 사진 리스트
PHOTO_LIST =[
"https://i.namu.wiki/i/rtpojRW_TWESwpHzBkyMSyvxQKV1VBVGjRgEEfntdRZKUyV5FjbysIZO57VSD6vFRY5oHA6pLdoQ78wXkcuHvqG6WtzP2xJyjvL49VCVDSsjnC3_tjLzCUTEPfQ7Rs1Nj1v7LJejafgkHmV7MxUwzw.webp",
"https://i.namu.wiki/i/jwCydBiKhFmq_v_rdPtva9LPopSF9lCMzyrVCcMlCFsxIMllCr7M3bTys5nSETxpMVe0DyD_7zUWcg1YL0I-CiyveKjxS7bJHPNov4Y26OuVBwfk6WiHRmX_g13jmz5171N2_yoJVFZZGv4dApqTqA.webp",
"https://i.namu.wiki/i/noJL_gjp3ufmugBW_iwkfLoSyI0hFHklMAzQ2gRWhty4Iw76_ShR-TM-BtlNoDom7osi-DozQwmq4QFoQn3SzW0jTn1poESBbCrVjDTVVFIBuRxpdBT-ASk3cBphv5RNV_m5jw5Jr__N1XhTDHBC9A.webp",
"https://i.namu.wiki/i/t6pIEfbyu7ta7Qf2tsmdUlGhBqYaU0fiDNu_m1LVzdEN_yt_sNALFqsquLsyAmoJadlf24HKrQlIppxGCXnHAEW_nGAxxp-RXt9bJ15vRlnigDcwt5V0KH6XLpappUi6yVGia0bpFFgk_WC8QPhWg.webp",
"https://i.namu.wiki/i/A1f8U9SlpnTaZhMU_iGdLx0XbIO51UQ2_oAOWFrcTGgwNPYrN-6soz8uSYf-JypaM0Jde5DRMgFnVc_dTdLiDpAB04sXDIhOG1HKqThik57EM2Z7Rn-OfEf9NpSaGBozcF5eD3xWfAnRk7_ZuygEzw.webp",
"https://i.namu.wiki/i/yfY_1N7sMiM14UgO1rCls-GrMxSjXkW7bzakm4l99kmdEL3uq5l_x8Pl4Fxf3ex5B3m3A4_Eqh42p85U9xify-9nvgHdcgGzhoZNnxWWNeUp2rAd5fy49sANUW-M-HJIITlZoe8gCgHfZpCF3th54A.webp"
]
async def start(update, context):
    await update.message.reply_text("안녕하세요! 저는 R_B봇 입니다. 무엇을 도와드릴까요?")


# async def send_photo(update, context):
#     photo_url = PHOTO_LIST
#     await update.message.reply_photo(photo=photo_url,caption="요청하신 이미지를 전송하였습니다.")

# /help 명령어에 대한 응답
async def help_command(update: Update, context: CallbackContext):
    help_text = (
        "🤖 R_B봇 사용법 🤖\n\n"
        "/start - 봇 시작하기\n"
        "/help - 명령어 목록 보기\n"
        "/music - 노래 추천\n"
        "\n💬 대화 명령어 💬\n"
        "안녕, 정보, 뭐해, 공격, 기분, 도움, 에러, 시작, 종료, 뭐지, 좋아, 싫어, 배고파, 졸려\n"
        "심심해, 고마워, 미안, 좋은 아침, 잘자, 뭐라고, 재밌다, 화났어, 귀엽다, 멋있다, 놀자, 심각해, 부탁해\n"
        "\n🍱 특별 명령어 🍱\n"
        "점심메뉴 - 오늘의 점심 추천 🍕\n"
        "사진줘 - 랜덤 사진 전송 📷\n"
        "gpt - gpt + 명령어 "
    )
    await update.message.reply_text(help_text)

# /music 명령어: 랜덤 음악 추천
async def music(update: Update, context: CallbackContext):
    music = random.choice(MUSIC_LIST)
    response = (
        f"🎶 오늘의 추천 음악 🎶\n\n"
        f"🎵 제목: *{music['title']}*\n"
        f"🎤 가수: {music['artist']}\n"
        f"🎸 장르: {music['genre']}\n"
        f"👉 [유튜브에서 듣기]({music['link']})"
    )
    await update.message.reply_text(response, parse_mode="Markdown", disable_web_page_preview=False)

# 일반 대화 감지 및 응답
async def monitor_chat(update: Update, context: CallbackContext):
    user_text = update.message.text  # 사용자가 입력한 메시지
    chat_id = update.message.chat_id  # 채팅방 ID

    # "gpt" 명령어 처리
    if "gpt" in user_text:
        res = gemini.aiai(user_text.replace("gpt ",""))
        await context.bot.send_message(chat_id=chat_id,text=res.replace("**",'')) # parse_mode="MarkdownV2"
    elif "사진줘" in user_text:
        photo_choice = random.choice(PHOTO_LIST)
        await context.bot.send_photo(chat_id=chat_id, photo=photo_choice, caption="📷 오늘의 사진 😆")
    # "점심메뉴" 명령어 처리
    elif "점심메뉴" in user_text:
        menu_choice = random.choice(LUNCH_MENU)
        await context.bot.send_message(chat_id=chat_id, text=f"🍱 오늘의 추천 점심: *{menu_choice}* 😋", parse_mode="Markdown")
        return
    else:
        # 트리거 단어 확인 (첫 번째로 발견된 단어에만 반응)
        for key, res in TRIGGER_WORDS.items():
            if key in user_text:
                await context.bot.send_message(chat_id=chat_id, text=res)
                break

def main():
    app = Application.builder().token(TOKEN).build()
    # 명령어 핸들러 추가
    app.add_handler(CommandHandler("start",start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("music", music))  # 음악 명령어 추가
    # 응답 핸들러 추가
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, monitor_chat))

    print("텔레그램 봇이 실행중입니다. 모니터링 중...")
    app.run_polling()
    
if __name__ == '__main__':
    main()