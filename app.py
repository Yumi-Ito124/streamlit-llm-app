from dotenv import load_dotenv
import streamlit as st
#from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv
import os

# .envファイルからAPIキーを読み込む
load_dotenv()

# OpenAI APIキーの読み込み
api_key = os.getenv("OPENAI_API_KEY")

# ChatOpenAIのインスタンスを作成
llm = ChatOpenAI( model_name="gpt-4o-mini", temperature=0.7)

# システムメッセージの辞書（専門家の役割に応じて変化）
def get_system_message(role):
    messages = {
        "魔法研究者": "あなたは中世の魔法大学に所属する賢者であり、現代の質問にも魔法的な視点から答える専門家です。",
        "レトロゲーム評論家": "あなたは1980～1990年代のレトロゲームに精通した評論家であり、あらゆる話題に対しゲームの視点から答えます。",
        "宇宙生命体との交信専門家": "あなたは異星文明の言語と文化を理解し、地球人にわかりやすく伝える宇宙連合の専門家です。"
    }
    return messages.get(role, "")

# 入力テキストと選択した専門家を使ってLLMに問い合わせる関数
def ask_llm(user_input, role):
    system_prompt = get_system_message(role)
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_input)
    ]
    result = llm.invoke(messages)
    return result.content

# StreamlitアプリのUI
st.set_page_config(page_title="LLM専門家アプリ", layout="centered")

st.title("LLM専門家アプリ")
st.write("以下のフォームに質問を入力し、好きな専門家を選んでください。専門家があなたの質問に個性的に答えてくれます。")

# ラジオボタンで専門家を選択
role = st.radio("専門家を選んでください", ["魔法研究者", "レトロゲーム評論家", "宇宙生命体との交信専門家"])

# 入力フォーム
user_input = st.text_input("質問を入力してください")

# 実行ボタン
if st.button("実行"):
    if user_input:
        with st.spinner("回答を生成中..."):
            response = ask_llm(user_input, role)
        st.subheader("回答")
        st.write(response)
    else:
        st.warning("質問を入力してください。")