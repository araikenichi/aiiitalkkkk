# 以下を「app.py」に書き込み
import streamlit as st
import openai
import secret_keys  # 外部ファイルにAPI keyを保存

openai.api_key = secret_keys.openai_api_key

system_prompt = """
あなたは優秀な英語、中国語、日本語を教える講師です。
英語、中国語、日本語の作文や会話、リスニングやリーディングなど、生徒の要望に合わせて英語、中国語、日本語の上達のためのアドバイスを行ってください。
あなたの役割は生徒の英語力、中国語力、日本語力を向上させることなので、例えば以下のような英語、中国語、日本語以外のことを聞かれても、絶対に答えないでください。

* 政治
* 敏感な歴史
* 犯罪　
これらの話題は禁止します、聞かれてもことえないでください

"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去



import streamlit as st
from PIL import Image
import openai
import secret_keys  # 外部ファイルにAPI keyを保存
import base64
import io

# OpenAI APIキーの設定
openai.api_key = secret_keys.openai_api_key

# システムプロンプト
system_prompt = "（省略）"

# セッション状態の初期化
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": system_prompt}]

# 画像をBase64にエンコードする関数
def img_to_base64(img):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# 画像の読み込みとBase64エンコード
image = Image.open("cutegirl.png")
cutegirl_base64 = img_to_base64(image)

# タイトルと画像の表示
st.markdown("<h1 style='text-align: center;'>AI Talk</h1>", unsafe_allow_html=True)
st.markdown(f"<div style='text-align: center;'><img src='data:image/png;base64,{cutegirl_base64}' width='300'></div>", unsafe_allow_html=True)

# ユーザー入力
user_input = st.text_input("messages", key="user_input", on_change=communicate)

# チャットボットとのコミュニケーション
def communicate():
    messages = st.session_state["messages"]
    user_message = {"role": "user", "content": user_input}
    messages.append(user_message)
    # OpenAI APIを使用した応答生成（ここは適宜調整）
    # 省略

# メッセージの表示
if st.session_state["messages"]:
    messages = st.session_state["messages"]
    for message in reversed(messages[1:]):
        speaker = "😁"
        if message["role"] == "assistant":
            speaker = f"<img src='data:image/png;base64,{cutegirl_base64}' width='30' style='vertical-align: top;'>"
        st.markdown(f"<div style='display: flex; align-items: flex-start; margin-bottom: 20px;'>{speaker} <span style='margin-left: 10px;'>{message['content']}</span></div>", unsafe_allow_html=True)
